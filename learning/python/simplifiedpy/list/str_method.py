#!/usr/bin/python
#Filename:str_methods.py

name='Swaroop'#this a string object
if name.startswith('Swa'):
    print "yes,the string start with 'Swa'"

if 'a' in name:
    print "Yes,it contains the string 'a'"

if name.find('war')!=-1:
    print 'Yes,it contains the string"war"'
delimiter='kill->'
mylist=['Brazil','Russia','India','China']
mylist.append(delimiter)
print mylist
print delimiter.join(mylist)
