#!/usr/bin/python
#Filename:backup_ver2.py
import os
import time
source=['/home/weijiayun/project/python/graphyplt/',
       '/home/weijiayun/project/python/simplifiedpy/']
target_dir='/home/weijiayun/project/python/backup/'
today=target_dir+time.strftime("%Y%m%d")
now=time.strftime("%H%M%S")
if not os.path.exists(today):
    os.makedirs(today)
    print 'Sucessfully created directory',today

target=today+os.sep+now+'.tar.bz2'#separation operator of directions,windows\\ mac OS :
zip_command="tar -jcv -f %s %s"%(target,' '.join(source))

if os.system(zip_command)==0:
    print 'Sucessful backup to',target
else:
    print 'Backup FAILED'



