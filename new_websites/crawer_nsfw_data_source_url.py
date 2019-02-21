#coding=utf-8
'''
Created on Feb 14, 2019

@author: root
'''
import os,threading,time
import os.path as op
import urllib2
import requests
import imghdr,cv2
from requests.adapters import HTTPAdapter



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pc_id=0
if pc_id==0:
    inpath=r'F:\workspaces\github\nsfw_data_source_urls-master/raw_data'
    outpath=r'E:\DL_datasets\nsfw_data_source_imgs'
elif pc_id==1: 
    inpath=r'/home/sherl/git/nsfw_data_source_urls/raw_data'
    outpath=r'/media/sherl/本地磁盘/data_DL/nsfw_data_source_imgs'

thread_maxcnt=24

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
proxy_dict_ss = {'http': 'socks5://127.0.0.1:1080','https':'socks5://127.0.0.1:1080'}#use local socket5 proxy,with shadowshocks
TIMEOUT=(10,40)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def getalltxtpath_and_outputpath(ind, outd):
    ret=[]
    for i in os.listdir(ind):
        tepin=op.join(ind, i)
        tepout=op.join(outd, i)
        
        if op.isdir(tepin):
            #if not op.exists(tepout): os.makedirs(tepout)
            ret+=getalltxtpath_and_outputpath(tepin, tepout)
        elif op.splitext(i)[-1] in ['.txt']:
            ret.append([tepin,outd])
    return ret
            
#paths=getalltxtpath_and_buildoutputpath(inpath , outpath)
#print paths[:5]
'''
examples:
http://2*.media.tumblr.com/b8192831bbbf40c64d9d9027aa092e02/tumblr_mi7btdQ4ui1rj6ivfo1_1280.jpg
'''
def imgfilecheck(fpath):
    try:
        tep=cv2.VideoCapture(fpath)
        if (not op.exists(fpath)) or op.getsize(fpath)<=1024 or \
        ( (cv2.imread(fpath) is None ) and (imghdr.what(fpath) is None) and (not tep.isOpened() ) ):
            if op.exists(fpath):os.remove(fpath)    #删除文件
            #print 'judge error:',imghdr.what(fpath)
            tep.release()
            return False
        tep.release()
        return True
    except Exception as e: 
        tep.release()
        print e
        return False

def oneurl_download(url, outp, proxy_dict=None):
    filename=op.split(url)[-1].split('?')[0]
    outfilename=op.join(outp, filename)
    
    req_sess = requests.Session()
    req_sess.mount('http://', HTTPAdapter(max_retries=3))
    req_sess.mount('https://', HTTPAdapter(max_retries=3))
        
    error_str=''
    error_code=200
    if op.exists(outfilename): 
        return True,error_code,error_str

    try:
        resp = req_sess.get(url,
                            stream=True,
                            proxies=proxy_dict,
                            headers=headers,
                            verify=False,
                            timeout=TIMEOUT,allow_redirects=True)
        error_code=resp.status_code
        if resp.status_code==302:
            location = resp.headers['Location'] # 注意有些header返回的Location中的url是不带host
            req_sess.close()
            return oneurl_download(location, outp, proxy_dict)
        elif resp.status_code !=requests.codes.ok:
            print("Access Error when retrieve %s,code:%d." % (url, resp.status_code))
            raise Exception("Access Error")
        else:
            print("Connect %s success." % (url))
            print 'writing to ',outfilename
        
            
            
        with open(outfilename, 'wb') as fh:
            for chunk in resp.iter_content(chunk_size=1024):
                fh.write(chunk)
                
    except Exception as e: 
        print (e)
        error_str=str(e)
        req_sess.close()
        # try again
        if proxy_dict is None:
            time.sleep(1)
            print 'exception happend:trying use proxy ...'
            return oneurl_download(url, outp, proxy_dict_ss)
        else:
            return False,error_code,error_str   
    #time.sleep(1)
    req_sess.close()
    return imgfilecheck(outfilename),error_code,error_str


def one_txt_download(txtpath, outp, index=0):
    if not op.exists(outp): os.makedirs(outp)
    
    error_fp=open(op.join(outp,'error_urls.txt'),'w+')
    cnt_true=0
    with open(txtpath,'r') as f:
        freadl=f.readlines()
        l=len(freadl)
        for ind,i in enumerate(freadl):
            print ind,'/',l
            tepi=i.strip()
            res,ecode,estr=oneurl_download(tepi, outp)
            
            if res:
                cnt_true+=1
                print 'thread:',index,':download ',tepi,' success'
            else:
                error_fp.write(tepi+' '+str(ecode)+' '+estr+'\n')
                print 'thread:',index,':download ',tepi,' failed'
            #time.sleep(1)
    print 'download ',txtpath,' done-->',cnt_true,'/',l
    error_fp.write(str(cnt_true)+'/'+str(l))
    error_fp.close()
    return cnt_true,l



def main():
    tcnt=0
    threadpool=[]
    nexti=False
    paths=getalltxtpath_and_outputpath(inpath , outpath)
    for ind,i in enumerate(paths):
        nexti=False
        if tcnt<thread_maxcnt:
            tcnt+=1
            print 'txt file cnts:',ind,'/',len(paths)
            print 'creating thread:',ind
            t = threading.Thread(target=one_txt_download, args=(i[0],i[1], ind))
            t.start()
            threadpool.append(t)
        else:
            while not nexti:
                for ind2 in range(len(threadpool)):
                    if not threadpool[ind2].isAlive():
                        print 'one thread down,creating thread :',ind
                        t = threading.Thread(target=one_txt_download, args=(i[0],i[1], ind))
                        t.start()
                        threadpool[ind2]=t
                        nexti=True
                        break
    for indd,i in enumerate(threadpool):
        print (indd,'/',len(threadpool),' waiting to stop..')
        i.join()
            
                
                

if __name__ == '__main__':
    #exam=r'http://25.media.tumblr.com/0fb48d97f5c8dbc19a372fb955930b74/tumblr_mllno9cuQk1ra163eo1_1280.jpg' 
    #oneurl_download(exam, r'E:\DL_datasets')
    main()
    
    print ('done..')





