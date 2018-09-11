'''
Created on Sep 11, 2018

@author: sherl
'''
import crawer_newsite as nt
import requests,sys,os,urllib
import os.path as op
#import uniout 
from bs4 import BeautifulSoup
import chardet,xlrd


url='http://openaccess.thecvf.com/content_ECCV_2018/html/'

def schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)

def first_page(url):
    txt,stat,code=nt.getpagewithdecode(url)
    sop=BeautifulSoup(txt,"html5lib")
    tep=sop.select('td a')
    
    ret=[]
    for i in tep:
        ret.append (i.get('href'))
    return ret[1:]
    
def sec_page(lists):
    for ind,i in enumerate(lists):
        txt,__,_ = nt.getpagewithdecode(i)
        sop=BeautifulSoup(txt,"html5lib")
        tep=sop.select('div[id="content"] a')[0].get('href')
        
        filname=op.join('./papers',(op.split(tep)[-1]))
        print (ind,'/',len(lists),'-->',filname)
        print (url+tep) 
        
        if not op.exists(filname):
            filepath, co = urllib.request.urlretrieve(url+tep, filname, schedule)
            #r=requests.get(url+tep,schedule)     
            print (ind,'/',len(lists),'-->',filepath,' http code:',co)
        else:
            print ('skip:',filname)

if __name__ == '__main__':
    sec_urls=first_page(url)
    sec_urls=list(map(lambda x:url+x, sec_urls))
    sec_page(sec_urls)
    