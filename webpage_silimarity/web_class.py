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
    '''
    1.提取function XXX()中的函数名字
    2.提取input等中的name属性
    3.提取href，src,background等中的链接，将链接分开去掉文件名，只提取具有的路径,如：a/b/c.html-->[a,b]
    4.提取class，id中的属性
    '''
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
        restr=r'(a|link|script|img).*?(href|src|background)\s*=\s*[\"|\']?(http[s]?:)?[\/|\\]*([\w|\_|\/|\\|\.]+)[\"|\'|\s|\?]+'
        
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
        return 0

def judge_nonull(htmldir):
    basepage=Website_pages(htmldir)
    for i in basepage.allnames:
        if len(basepage.allnames[i])<=1: return False
    return True


def get_groups(dislist, gap=0.1):#将结果分组
    distsorte=np.sort(dislist)
    argss=dislist.argsort()
    
    ret=[[]]
    tep=float(distsorte[0])
    cnt=1
    for inx,i in enumerate(distsorte):
        if abs(tep/cnt-i)>=gap:
            tep=i
            cnt=1
            ret.append([])
        tep+=i
        cnt+=1
        ret[-1].append(argss[inx])
    return ret

def merge_groups(group1,group2):#合并俩个group,由两个分组合成新的分组
    ret=[]
    for i in group1:
        iset=set(i)
        
        for j in group2:#将1中的每一行与2中每一行获取交集作为一个新的分组
            tepset=set(j)
            t=iset.intersection(tepset)
            if len(t)>0: ret.append(t)
            iset.difference_update(tepset)
        
        if len(iset)>0:
            ret.append(iset)
            
    return ret
            
#---------------------------------------------------------------------#   panel      
dir_web=u'F:\网络中心\网站相似度匹配\第一批首页'
#dir_web=u'E:\wokmaterial\emergencyCenter\第一批首页'



#---------------------------------------------------------------------#
dirlis=map(lambda x:op.join(dir_web, x),os.listdir(dir_web))      

feather_list=[]
for i in dirlis:
    feather_list.append(Website_pages(i))

fp=open("./log.txt","w+")

def get_overlaprate(basepage_id):#获取选定网页与所有的重叠度
    veclis=[]
    basepage=feather_list[basepage_id]   #Website_pages(dirlis[basepage_id])
        
    for ind,i in enumerate(dirlis):
        #tep=Website_pages(i)
        tep=feather_list[ind]
        veclis.append(basepage.compare_to(tep))
    return veclis
         
         


    
def start( threshhold):    #这里可以设置阈值，即距离达到多少判定为一组
    basepage_id=0
    
    group_list=[]
    
    while basepage_id<len(dirlis):
        if  not judge_nonull(dirlis[basepage_id]):#get a page that without null list
            basepage_id+=1
            continue
        
        
        print '\nchoose:',basepage_id
        print dirlis[basepage_id]
        
        veclis=get_overlaprate(basepage_id)#获取选定网页与所有的重叠度
        
        print 'get vector len:',len(veclis)
        
        dislist=np.array(map(lambda x:cosdistance(x,veclis[basepage_id]), veclis))
        #dis_eurolist=np.array(map(lambda x:Euclidean_Distance(x,veclis[basepage_id]), veclis))
        
        
        #sortedd=np.sort(dislist)
        #args=dislist.argsort()
        
        retgroups=get_groups(dislist, threshhold)#这里可以设置阈值，即距离达到多少判定为一组
        
        group_list=merge_groups(retgroups,group_list)
        
        print 'groups:',len(group_list),"  with threshold:",threshhold
        
        cnt_len=0
        for i in group_list:
            if len(i)>1: 
                cnt_len+=1
                #print i
                
                for j in i:
                    #print "-->",dirlis[j]
                    pass
        
        basepage_id+=1
        #print args
        #plt.plot(sortedd, 'r.')
        #plt.show()
        
        '''
        basepage.printout()
        for ind,i in enumerate(sortedd):
            if i>0.1:
                tepdir=dirlis[args[ind]]
                print tepdir,":",i
                if ind<len(sortedd)-1:
                    print "前后俩个欧式距离为：",Euclidean_Distance(veclis[args[ind]],veclis[args[ind+1]])
                tep=Website_pages(op.join(dir_web,tepdir))
                tep.printout()
                print basepage.compare_to(tep),'\n'
        '''
    print "the final groups len:",len(group_list)," with threshhold:",threshhold," len>2 is:",cnt_len
    return group_list




def cosdistance(lis1,lis2):#相似度最大为1，越大越相似
    x=np.array(lis1)
    y=np.array(lis2)
    
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
        
    
        
        
def Euclidean_Distance(lis1,lis2):#欧式距离,越小越相似
    x=np.array(lis1)
    y=np.array(lis2)
    #print x.dtype
    return np.linalg.norm( x - y )
        

def compare2groups(group1, group2, dirlis):#以group1为主，比较group2与1的区别
    if len(group1)<=0 or len(group2)<=0:
        return None
    fp.write('\n\ncompare start!\n')
    for i in group2:
        tepi=set(i)
        
        for j in group1:
            tepj=set(j)
            ins=tepi.intersection(tepj)#交际
            
            if len(ins)>0 and (len(tepi) + len(tepj))>2 and not(len(ins)==len(tepi) and len(ins)==len(tepj)):
                print '\ngroup2:',tepi,'\nlen:',len(tepi)," 中："
                print "-->",ins," len:",len(ins)," in:"
                print "---->group1",tepj," len:",len(tepj)
                
                print "-->",map(lambda x:op.split(dirlis[x])[-1], ins)
                print "---->",map(lambda x:op.split(dirlis[x])[-1], tepj)
                
                fp.write( '\ngroup2:'+str(tepi)+'\nlen:'+str(len(tepi))+' 中：\n')
                fp.write( "-->"+str(ins)+" len:"+str(len(ins))+' in:\n')
                fp.write( "---->group1"+str(tepj)+" len:"+str(len(tepj))+'\n')
                
                fp.write( "-->"+str(map(lambda x:op.split(dirlis[x])[-1], ins))+'\n')
                fp.write( "---->"+str(map(lambda x:op.split(dirlis[x])[-1], tepj))+'\n')
    
        
    
    
        

if __name__ == '__main__':
    '''
    tep=Website_pages(u'E:\wokmaterial\emergencyCenter\第一批首页/102.html')
    tep.printout()
    
    tep2=Website_pages(u'E:\wokmaterial\emergencyCenter\第一批首页/104.html')
    tep2.printout()
    
    
    vec=tep.compare_to(tep2)
    print cosdistance(vec,vec)
    '''
    before=[]
    lenlis=[]
    for i in range(1,50):
        tep=start( float(i)/100)
        lenlis.append(len(tep))
        compare2groups(before, tep, dirlis)
        fp.write("compare to group2 with threshhold:"+str(float(i)/100)+ " done!\n\n\n\n")
        
        before=tep
        
    plt.plot(range(len(lenlis)), lenlis)
    plt.show()
    
    fp.close()
        
    #print tep.overlap_rate(['aa','bdd','cd'], ['aa','bb','cc'])
    
    #print tep.gethref_name(r'<SCRIPT src="/js/comm/md5.js" type=text/javascript ></SCRIPT>')
    