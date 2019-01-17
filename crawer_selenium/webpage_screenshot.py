#coding:utf-8
'''
Created on 2019年1月17日

@author: sherl
'''

from selenium import webdriver
import time,os
import chardet,xlrd
import os.path as op
#from pyvirtualdisplay import Display

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('headless')
#chrome_options.add_argument('no-sandbox')

savedir='./result_screenshot'
if not op.exists(savedir): os.makedirs(savedir)

excel_path=''


def capture(url):
    browser = webdriver.Chrome(chrome_options=chrome_options) # Get local session of chrome
    browser.set_window_size(800, 600)
    browser.get(url) # Load page
  
    time.sleep(3)
  
    try:
        picture_url=browser.save_screenshot(op.join(savedir ,url+'.png'))
        print("%s ：截图成功！！！" % picture_url)
    except BaseException as msg:
        print("%s ：截图失败！！！" % msg)
    browser.close()
    
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
    pass