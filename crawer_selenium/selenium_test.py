#coding:utf-8
'''
Created on Aug 28, 2018

@author: root
'''

from selenium import webdriver
#from pyvirtualdisplay import Display

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')


#display = Display(visible=0, size=(800, 800))  
#display.start()
#browser = webdriver.PhantomJS()
browser = webdriver.Chrome(chrome_options=chrome_options)#

browser.get("http://www.baidu.com")
print(browser.page_source)
print (browser.title)
browser.close()

if __name__ == '__main__':
    pass