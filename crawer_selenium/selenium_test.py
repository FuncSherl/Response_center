#coding:utf-8
'''
Created on Aug 28, 2018

@author: root
'''

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get("http://www.baidu.com")
print(browser.page_source)
browser.close()

if __name__ == '__main__':
    pass