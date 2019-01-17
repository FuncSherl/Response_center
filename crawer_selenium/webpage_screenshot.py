#coding:utf-8
'''
Created on 2019年1月17日

@author: sherl
'''

from selenium import webdriver
import time,os,re
import chardet,xlrd,xlwt
import os.path as op
#from pyvirtualdisplay import Display

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
#chrome_options.add_argument('no-sandbox')

savedir=op.join(os.getcwd(), 'result_screenshot')
if not op.exists(savedir): os.makedirs(savedir)

excel_path='./hnyx-ips.xlsx'
timeout=3


def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True  
    else:  
        return False


def capture(url):
    browser = webdriver.Chrome(chrome_options=chrome_options) # Get local session of chrome
    #browser.set_window_size(800, 600)
    browser.maximize_window()
    #browser.set_page_load_timeout(5) #
    
    browser.implicitly_wait(timeout)
    try:
        browser.get(url) # Load page
    except BaseException as msg:
        print ('Error:%s'%msg)
        browser.close()
        return False
  
    #time.sleep(3) #等待网页加载完成
    
    print ('loading...')
    imgname=url.replace(':','-').replace('.','_').replace('/','')
    imgname=op.join(savedir ,imgname+'.png')
    picture_url=browser.save_screenshot(imgname)
    if picture_url: 
        print('Success->%s:%s' % (imgname, browser.title))
    else:
        print('!!!Error->%s:%s' % (url,imgname))
    browser.close()
    
    return True
    
def getiplist(excel_p=excel_path):
    data=xlrd.open_workbook(excel_p)
    table=data.sheets()[0]
    
    
    for i in range(1,table.nrows):
        #print table.cell(1,2).value
        tep=table.row_values(i)
        
        ipaddr=tep[0]

        ipaddr='http://'+ipaddr
            
        ip_d=ipaddr+":"+str(int(tep[1]))
        print ('\nprocing:'+ip_d)
        capture(ip_d)
            
        


if __name__ == '__main__':
    #capture('http://www.baidu.com')
    getiplist()
    pass


