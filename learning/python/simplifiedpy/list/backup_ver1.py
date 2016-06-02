#!/usr/bin/python
#Filename:backup_ver1.py

import os
import time

source=['/home/weijiayun/project/python/graphyplt/',
       '/home/weijiayun/project/python/simplifiedpy']
target_dir='/home/weijiayun/project/python/'

target=target_dir+'python'+time.strftime('%Y%m%d%H%M')+'.tar.bz2'
zip_command="tar -jcv -f %s %s"%(target,' '.join(source))

if os.system(zip_command)==0:
    print 'Sucessful backup to',target
else:
    print 'Backup FAILED'


