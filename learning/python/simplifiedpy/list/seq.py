#!/usr/bin/python
#Filename:seq.py

shoplist=['apple','mango','carrot','banana']
#Indexing or "Subscription"operation
print 'Item 0 is',shoplist[0]
print 'Item 1 is',shoplist[1]
print 'Item 2 is',shoplist[2]
print 'Item 3 is',shoplist[3]
print 'Item -1 is',shoplist[-1]
print 'Item -2 is',shoplist[-2]

#Slicing on a list
print 'Item 1 to 3 is',shoplist[1:3]
print 'Item 2 to end is',shoplist[1:]
print 'Item 1 to -1 is',shoplist[0:-1]
print 'Item start to end is',shoplist[:]

#Slicing on a string
name='Swaroop'
print 'character 1 to 3 is',name[1:3]
print 'character 2 to end is',name[1:]
print 'character 1 to -1 is',name[0:-1]
print 'character start to end is',name[:]

