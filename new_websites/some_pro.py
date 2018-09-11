'''
Created on Sep 11, 2018

@author: root
'''
import os,chardet
import os.path as op

indir='./first_pages'
outdir='./test_addpages'

for i in os.listdir(indir):
    tep=op.join(indir, i)
    print (tep)
    with open(tep,'rb') as f:
        strr=f.read()
        
        enc=chardet.detect(strr)['encoding']
        if enc:
            strr=strr.decode(enc,errors = 'ignore')
            with open(op.join(outdir, i),'w+',encoding='utf-8') as f2:
                f2.write(strr)
        


if __name__ == '__main__':
    pass