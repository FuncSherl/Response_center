#coding:utf-8
'''
Created on 2018��7��11��

@author: sherl
'''
import re,os
import os.path as op
import numpy as np
import matplotlib.pyplot as plt

class Website_pages:
    def __init__(self,pagedir):
        self.allnames={}
        
        self.allnames["fun_names"]=[]#stroe function names
        self.allnames["input_names"]=[]#input name
        self.allnames["href_names"]=[]#to href
        self.allnames["id_class_names"]=[]
        #self.
        
        self.feed(pagedir)
        pass
    
    def printout(self):
        for i in self.allnames:
            print i,":",self.allnames[i]
            
            
    def feed(self,pagedir):
        with open(pagedir,"r") as f:
            for line in f.readlines():
                tepline=line.strip()
                
                self.allnames["fun_names"].extend((self.getfun_names(tepline)))#add function names
                self.allnames["input_names"].extend((self.getinput_names(tepline)))
                self.allnames["href_names"].extend(self.gethref_name(tepline))#add href dir
                self.allnames["id_class_names"].extend(self.getclass_id_names(tepline))#id or class names
                
                
                for i in self.allnames:
                    self.allnames[i]=list(set(self.allnames[i]))
                '''
                self.allnames["fun_names"]=list(set(self.allnames["fun_names"]))
                self.allnames["input_names"]=list(set(self.allnames["input_names"]))
                self.allnames["href_names"]=list(set(self.allnames["href_names"]))
                self.allnames["id_class_names"]=list(set(self.allnames["id_class_names"]))
                '''
                
                
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
    
    def getclass_id_names(self,instr):#<div class="am-g" style="position: relative; top:60px">
        #<div id="systitlecontainer">   <input id="loginid" type="text" class="loginipt" value="请输入用户名" />
        # <td class="chklab">记住密码</td>
        #<iframe id="ifrmRegister" frameborder="0" style="width:100%;height:100%;"></iframe>
        restr=r'\b(id|class)\s*=\s*[\"|\']?([\w|\_|\s]+)[\"|\'|=]'
        it=re.finditer(restr, instr, re.I)
        teplist=self.get_from_iter(it,2)
        
        retlist=[]
        for i in teplist:
            retlist.extend(i.strip().split())
            
        return retlist
    
        
        
            
    def get_from_iter(self,it,groupid=1):#从re的iter中取names
        retnames=[]
        if it:
            for i in it:
                #print i.group()
                #self.fun_names.append(i.group(1).strip())
                retnames.append(i.group(groupid).strip())
            
        #print retnames
        return retnames
    
    
    def compare_to(self,anoclass):
        ret=[]
        for i in self.allnames:
            ret.append(self.overlap_rate(self.allnames[i], anoclass.allnames[i]))
        return ret
        
    
    def overlap_rate(self,lis1,lis2):#重叠度
        overlap=0
        for i in lis1:
            if i in lis2:
                overlap+=1
        
        if len(lis1)+len(lis2)>0:        
            return float(overlap)/(len(lis1)+len(lis2)-overlap)
        return 1
        
    
def start(dir):  
    basepage_id=1
    
    
    veclis=[]
    dirlis=map(lambda x:op.join(dir, x),os.listdir(dir))
    basepage=Website_pages(dirlis[basepage_id])
    
    for i in dirlis:
        tep=Website_pages(op.join(dir,i))
        veclis.append(basepage.compare_to(tep))
        print 'do:',i
    
    print 'get vectors:',len(veclis)
    
    dislist=np.array(map(lambda x:cosdistance(x,veclis[basepage_id]), veclis))
    
    sortedd=np.sort(dislist)
    args=dislist.argsort()
    
    print args
    #plt.plot(sortedd, 'r.')
    #plt.show()
    for ind,i in enumerate(dislist):
        if i>0.8:
            print dirlis[ind]
            




def cosdistance(lis1,lis2):#相似度最大为1，越大越相似
    x=np.array(lis1)
    y=np.array(lis2)
    
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
        
    
        
        
def Euclidean_Distance(lis1,lis2):#欧式距离,越小越相似
    x=np.array(lis1)
    y=np.array(lis2)
    #print x.dtype
    return np.linalg.norm( x - y )
        
    
    
    
        

if __name__ == '__main__':
    paths=u'E:\wokmaterial\emergencyCenter\第一批首页'
    '''
    tep=Website_pages(u'E:\wokmaterial\emergencyCenter\第一批首页/102.html')
    tep.printout()
    
    tep2=Website_pages(u'E:\wokmaterial\emergencyCenter\第一批首页/104.html')
    tep2.printout()
    
    
    vec=tep.compare_to(tep2)
    print cosdistance(vec,vec)
    '''
    start(paths)
    #print tep.overlap_rate(['aa','bdd','cd'], ['aa','bb','cc'])
    
    #print tep.gethref_name(r'<SCRIPT src="/js/comm/md5.js" type=text/javascript ></SCRIPT>')
    