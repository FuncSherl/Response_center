#coding:utf-8
'''
Created on Aug 31, 2018

@author: root
'''

import requests,sys,os
#import uniout 
from bs4 import BeautifulSoup
import chardet,xlrd


headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


def getpagewithdecode(url):
    #r = requests.get("http://httpbin.org/get", params=payload, headers=headers,data='this is data')
    try:
        #这一 timeout 值将会用作 connect 和 read 二者的 timeout。如果要分别制定，就传入一个元组
        r = requests.get(url,headers=headers,timeout=(3,30))

    except Exception as e:
        return repr(e),False
    else:
        tep= r.content
        r.encoding=chardet.detect(tep)['encoding']
        return r.text,True

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
    url=[x[0] for x in excel_list]
    print (url)
    
    log=open("./pages/results.txt","a+", encoding='utf-8')
    #url=['192.168.1.1','www.baidu.com']
    for ind,i in enumerate(url):
        htt='http://'+i
        
        print (htt)
        
        tep,stat=getpagewithdecode(htt)
        #print tep
        #print (parse_page(tep))
        #print (excel_list[ind])
        if stat:
            with open("./pages/"+str(ind)+".txt", 'w+', encoding='utf-8') as f: f.write(tep)
        else:
            log.write(str(ind)+"  "+htt+"  "+tep+'\n')
        
    log.close()
    
    
    
    
    
    
    
    
    