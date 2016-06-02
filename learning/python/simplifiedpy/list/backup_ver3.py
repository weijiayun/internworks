#!/usr/bin/python
#Filename:backup_ver3.py
import os
import time
import sys
source=sys.argv[1:]
include=[]
exclustr=[]
print source[2]
for str in source:
    if str.find('*.py~')!=-1:
        exclustr.append(str)
        print 'ok'
    else:
        include.append(str)
print exclustr
print include
target_dir='/home/weijiayun/project/python/backup/'
today=target_dir+time.strftime("%Y%m%d")
now=time.strftime("%H%M%S")
comment=raw_input('Enter a comment-->')
if len(comment)==0:
    target=today+os.sep+now+'.tar.bz2'#separation operator of directions,windows\\ mac OS :
else:
    target=today+os.sep+now+'_'+\
            comment.replace(' ','_')+'.tar.bz2'#separation operator of directions,windows\\ mac OS :
if not os.path.exists(today):
    os.makedirs(today)
    print 'Sucessfully created directory',today
if len(exclustr):
    zip_command="tar -jcv -f %s %s --exclude=%s"\
        %(target,' '.join(include),' --exclude='.join(exclustr))
else:
    zip_command="tar -jcv -f %s %s"%(target,' '.join(include))
    

if os.system(zip_command)==0:
    print 'Sucessful backup to',target
else:
    print 'Backup FAILED'




