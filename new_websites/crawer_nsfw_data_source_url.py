#coding=utf-8
'''
Created on Feb 14, 2019

@author: root
'''
import os
import os.path as op
import urllib2
import requests
import imghdr,cv2
from requests.adapters import HTTPAdapter

req_sess = requests.Session()
req_sess.mount('http://', HTTPAdapter(max_retries=3))
req_sess.mount('https://', HTTPAdapter(max_retries=3))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
inpath=r'/home/sherl/git/nsfw_data_source_urls/raw_data'
outpath=r'/media/sherl/本地磁盘1/data_DL/nsfw_data_source_imgs'

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
proxy_dict = {'http': 'socks5://127.0.0.1:1080','https':'socks5://127.0.0.1:1080'}#use local socket5 proxy,with shadowshocks
TIMEOUT=(20,30)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def getalltxtpath_and_buildoutputpath(ind, outd):
    ret=[]
    for i in os.listdir(ind):
        tepin=op.join(ind, i)
        tepout=op.join(outd, i)
        
        if op.isdir(tepin):
            if not op.exists(tepout): os.makedirs(tepout)
            ret+=getalltxtpath_and_buildoutputpath(tepin, tepout)
        elif op.splitext(i)[-1] in ['.txt']:
            ret.append([tepin,outd])
    return ret
            
#paths=getalltxtpath_and_buildoutputpath(inpath , outpath)
#print paths[:5]
'''
examples:
http://24.media.tumblr.com/b8192831bbbf40c64d9d9027aa092e02/tumblr_mi7btdQ4ui1rj6ivfo1_1280.jpg
'''
def imgfilecheck(fpath):
    if (not op.exists(fpath)) or op.getsize(fpath)<=1024 or ( cv2.imread(fpath) is None):
        if op.exists(fpath):os.remove(fpath)    #删除文件
        #print 'judge error:',imghdr.what(fpath)
        return False
    return True

def oneurl_download(url, outp, proxy_dict=None):
    filename=op.split(url)[-1].split('?')[0]
    outfilename=op.join(outp, filename)
    
    if imgfilecheck(outfilename): 
        return True
    
    try:
        resp = req_sess.get(url,
                            stream=True,
                            proxies=proxy_dict,
                            headers=headers,
                            verify=False,
                            timeout=TIMEOUT)
        
        if resp.status_code !=requests.codes.ok:
            print("Access Error when retrieve %s,code:%d." % (url, resp.status_code))
            raise Exception("Access Error")
        else:
            print("Connect %s success." % (url))
            print 'writing to ',outfilename
        
            
            
        with open(outfilename, 'wb') as fh:
            for chunk in resp.iter_content(chunk_size=1024):
                fh.write(chunk)
                
    except :
        # try again
        if not proxy_dict:
            print 'trying use proxy ...'
            return oneurl_download(url, outp, proxy_dict=proxy_dict)
        else:
            return False   
    return imgfilecheck(outfilename)


def one_txt_download(txtpath, outp):
    cnt_true=0
    with open(txtpath,'r') as f:
        freadl=f.readlines()
        l=len(freadl)
        for ind,i in enumerate(freadl):
            print ind,'/',l
            tepi=i.strip()
            res=oneurl_download(tepi, outp)
            
            if res:
                cnt_true+=1
                print 'download ',i,' success'
            else:
                print 'download ',i,' failed'
    print 'download ',txtpath,' done-->',cnt_true,'/',l
    return cnt_true,l

def main():
    paths=getalltxtpath_and_buildoutputpath(inpath , outpath)
    for ind,i in enumerate(paths):
        print 'txt file cnts:',ind,'/',len(paths)
        one_txt_download(*i)

if __name__ == '__main__':
    main()





