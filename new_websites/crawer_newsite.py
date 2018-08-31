#coding:utf-8
'''
Created on Aug 31, 2018

@author: root
'''

import requests
 
payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers,data='this is data')
print r.url
print r.text

r = requests.get('https://inv-veri.chinatax.gov.cn/', verify=True)
print r.text

if __name__ == '__main__':
    pass