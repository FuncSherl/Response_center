#coding:utf-8
'''
Created on Aug 31, 2018

@author: root
'''

import requests,sys,os
import os.path as op
#import uniout 
from bs4 import BeautifulSoup
import chardet,xlrd

###########################################################################################################################panel

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
proxy_dict = {'http': 'socks5://127.0.0.1:1080','https':'socks5://127.0.0.1:1080'}#use local socket5 proxy,with shadowshocks
timeout=(20,30)

###########################################################################################################################

def getpagewithdecode(url):
    #r = requests.get("http://httpbin.org/get", params=payload, headers=headers,data='this is data')
    try:
        #这一 timeout 值将会用作 connect 和 read 二者的 timeout。如果要分别制定，就传入一个元组
        r = requests.get(url,headers=headers,timeout=timeout, verify=False)#,proxies=proxy_dict

    except Exception as e:
        return repr(e),-1,False
    else:
        tep= r.content
        r.encoding=chardet.detect(tep)['encoding']
        return r.text,r.status_code,True

def parse_page(pagestr):
    '''
    if type(soup.a.string)==bs4.element.Comment:
        print soup.a.string
        
        <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
    Elsie
    '''
    sop=BeautifulSoup(pagestr,"html5lib")
    #print sop.prettify(encoding='utf-8')
    '''
    for child in sop.descendants:
        print child
    '''
    return sop.title

def getiplist(excel_p):
    data=xlrd.open_workbook(excel_p)
    table=data.sheets()[0]
    
    ret=[]
    for i in range(1,table.nrows):
        #print table.cell(1,2).value
        tep=table.row_values(i)
        
        ip_d=[tep[0]+":"+str(int(tep[1])), (tep[2]), tep[3]]
        ret.append( ip_d)
        
    return ret
    
    



if __name__ == '__main__':
    excel_path=r'./ip_list.xlsx'
    resultdir='./pages'
    
    if not os.path.isdir(resultdir):
        os.makedirs(resultdir)
    
    excel_list=getiplist(excel_path)
    '''
    for i in excel_list:
        print (i)
    exit()
    '''
    url=[x[0] for x in excel_list]
    
    log=open(  "./results.txt"  ,"a+", encoding='utf-8')
    #url=['192.168.1.1','www.baidu.com']
    err_cnt=0
    skipcnt=0
    newadd=0
    for ind,i in enumerate(url):
        htt=i
        
        str_txt=op.join(resultdir,str(ind)+ '_'+i +".txt")
        
        if not i.startswith('http'):
            if int(i.split(':')[-1].strip())==443:
                htt='https://'+i
            else :htt='http://'+i
            
        else: str_txt=op.join(resultdir,str(ind)+".txt")
        
        print (htt+"   "+str(ind)+"/"+str(len(url)))
        
        if not os.path.exists(str_txt):#if this url is parsed
            tep,httpcode,stat=getpagewithdecode(htt)
            #print tep
            #print (parse_page(tep))
            #print (excel_list[ind])
            if stat:
                newadd+=1
                with open(  str_txt, 'w+', encoding='utf-8') as f: f.write(tep)
                print ('code:',httpcode,'  done!')
            else:
                err_cnt+=1
                log.write(str(ind)+"  code:"+str(httpcode)+'   '+htt+"  "+tep+'\n')
                print ('code:',httpcode,'  ',tep)
        else:
            skipcnt+=1
            print ('already exists,skiping:',skipcnt)
        print ("states:"+str(stat)+"   error count:"+str(err_cnt)+'\n')
        
    print ("crawer done,newadd:",newadd)
    log.close()
    
    
    
    
    
    
    
    
    