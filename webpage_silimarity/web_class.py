#coding:utf-8
'''
Created on 2018��7��11��

@author: sherl
'''
import re

class Website_pages:
    def __init__(self,pagedir):
        self.fun_names=[]#stroe function names
        #self.
        
        self.feed(pagedir)
        pass
    
    def feed(self,pagedir):
        with open(pagedir,"r") as f:
            for line in f.readlines():
                tepline=line.strip()
                
                self.fun_names.extend((self.getfun_names(tepline)))#add function names
                
            
            
    def getfun_names(self,instr):#获取 function XXXX（）形式中的函数名：eg. function Clear() {
        restr=r'function\s+([\w|\_]+)\s*\('
        retnames=[]
        
        it=re.finditer(restr, instr)
        if it:
            for i in it:
                #print i.group()
                #self.fun_names.append(i.group(1).strip())
                retnames.append(i.group(1).strip())
            
        #print retnames
        return retnames
        
        

if __name__ == '__main__':
    tep=Website_pages(u'F:/网络中心/网站相似度匹配/第一批首页/181.html')
    print tep.fun_names
    pass