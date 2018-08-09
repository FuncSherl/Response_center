#coding:utf-8
'''
Created on 2018年8月7日

@author:China
'''
import numpy as np
import matplotlib.pyplot as plt


def Distance(vec1, vec2):
    # 计算向量vec1和向量vec2之间的欧氏距离
    return np.sqrt(np.sum(np.square(vec1 - vec2)))

def cal_mean_square(vec_lis, core):
    '''
            计算一个中心的均方误差
    input:
            数据列表vec_lis
            中心点core
    '''
    dist=0.0
    for i in vec_lis:
        dist+=Distance(i, core)
    return dist

def cal_all_cores_dis(dat, groups, cores):#
    '''
    calculate all groups' distance
    '''
    if len(groups)!=len(cores): 
        print "error len(groups)!=len(cores)"
        return None
    ret=0
    for ind,i in enumerate(groups):
        ret+=cal_mean_square(list(map(lambda x:dat[x], i)), cores[ind])
        
    return ret


def forward_once(dat, cores):
    groups=[]
    for i in range(len(cores)):
        groups.append([])
    
    for ind,i in enumerate(dat):
        disind=np.array(map(lambda x:Distance(i,x), cores)).argmax()
        groups[disind].append(ind)
        cores[disind]=(i+cores[disind])/2
        #print 'cores:',cores
        #print groups
    
    return groups,cores
        

def classify(dat, k=5,threshhold=0.001):
    '''
    input:a 2-D vector and every item is the same length list 
        k:group nums
        threshhold:when to stop
    reuturn:a 2-D vector: groups that divided
    '''
    if len(dat)<=0 or len(dat[0])<=0: return []
    
    tep_dat=np.array(dat)
    
    min_item=tep_dat.min()
    max_item=tep_dat.max()#最大值与最小值
    
    print ("kmeans:min->max",min_item,"->",max_item)
    item_l=len(dat[0])#元素长度
    
    k_vec=(max_item-min_item)*np.random.random([k,item_l])+min_item#随机的k个向量中心点
    print k_vec
    
    groups,k_vec=forward_once(tep_dat, k_vec)
    new_dis=cal_all_cores_dis(tep_dat, groups, k_vec)
    old_dis=new_dis+threshhold+1
    
    cnt=0
    
    while abs(new_dis-old_dis)>threshhold:
        old_dis=new_dis
        groups,k_vec=forward_once(tep_dat, k_vec)
        new_dis=cal_all_cores_dis(tep_dat, groups, k_vec)
        cnt+=1
        
        print ("process ",cnt)
        for i in groups:
            print ("len:",len(i),'groups:',i)
        print ("cores:",k_vec)
        print ("distance sum:",new_dis)
        
    return groups,k_vec
    

    
    
    

if __name__ == '__main__':
    dat=np.random.random([100, 2])
    groups, cores=classify(dat)
    
    plt.scatter(dat[:,0], dat[:,1], c='blue',s=1,marker='.')
    plt.scatter(cores[:,0],cores[:,1],c='red')
    
    plt.show()
    
    
    