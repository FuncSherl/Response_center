#coding:utf-8
'''
Created on 2018��7��11��

@author: sherl
'''
import re

class Website_pages:
    def __init__(self,pagedir):
        self.fun_names=[]#stroe function names
        self.input_names=[]#input name
        self.href_names=[]#to href
        #self.
        
        self.feed(pagedir)
        pass
    
    def feed(self,pagedir):
        with open(pagedir,"r") as f:
            for line in f.readlines():
                tepline=line.strip()
                
                self.fun_names.extend((self.getfun_names(tepline)))#add function names
                self.input_names.extend((self.getinput_names(tepline)))
                self.href_names.extend(self.gethref_name(tepline))#add href dir
                
                
                
                self.fun_names=list(set(self.fun_names))
                self.input_names=list(set(self.input_names))
                self.href_names=list(set(self.href_names))
                
                
                
    def getinput_names(self,instr):#<input name="tbox_pwd" type="password" id="tbox_pwd" class="dh_login_text" value="" />
        restr=r'input.*?name\s*=\s*[\"|\']?([\w|\_]+)[\"|\'|\s]*'
        it=re.finditer(restr, instr, re.I)
        return self.get_from_iter(it)
        
           
            
    def getfun_names(self,instr):#获取 function XXXX（）形式中的函数名：eg. function Clear() {
        restr=r'function\s+([\w|\_]+)\s*\('
        
        it=re.finditer(restr, instr, re.I)
        return self.get_from_iter(it)
        
        
    def gethref_name(self,instr):#<link href="MonitorResource/login.css" rel="stylesheet" type="text/css" />    
        #<a href="Resource/Silverlight.exe" target="_blank">Siverlight控件下载</a>
        restr=r'(a|link|script|img).*?(href|src|background)\s*=\s*[\"|\']?(http[s]?:)?[\/|\\]*([\w|\_|\/|\\|\.]+)[\"|\'|\s]+'
        
        it=re.finditer(restr, instr,re.I)
        tep=self.get_from_iter(it,4)
        #print tep
        retstr=[]
        for i in tep:
            tepre=(re.split(r'[\\|\/]',i))
            #print tepre
            
            tepre=tepre[0:-1]#get the dir
            #print tepre
            retstr.extend(tepre)
        
        return retstr
        
        
            
    def get_from_iter(self,it,groupid=1):#从re的iter中取names
        retnames=[]
        if it:
            for i in it:
                #print i.group()
                #self.fun_names.append(i.group(1).strip())
                retnames.append(i.group(groupid).strip())
            
        #print retnames
        return retnames
        

if __name__ == '__main__':
    tep=Website_pages(u'F:/网络中心/网站相似度匹配/第一批首页/98.html')
    print tep.fun_names
    print tep.input_names
    print tep.href_names
    
    #print tep.gethref_name(r'<SCRIPT src="/js/comm/md5.js" type=text/javascript ></SCRIPT>')
    pass