#!/usr/bin/python
#Filename:using_file.py

poem='''\
Programming id fun 
When we work is done
if you wanna make your work also fun
      using PYTHON!
'''
f=file('poem.txt','w')
f.write(poem)
f.close

f=open('poem.txt','a+')
poem2='May the force be with you!My master!'
f.write(poem2)
f.close()
f=open('poem.txt')
while True:
    line=f.readline()
    if len(line)==0:#Zero length indicates EOF
        break
    print line,
f.close()
