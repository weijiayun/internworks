#!/usr/bin/python
#Filename:lambda.py

def make_repeater(n): 
    return lambda s:s*n    #return s*n s is the argument of new function
twice=make_repeater(2)     #where twice is a function return by make_repeater( )


print twice('word')
print twice(5)
a='print "hello the world"'
exec a #execute commands in the characters
b='2*3+4'
print eval(b) #execute significant expression of python in characters
mylist=['item','wei','jia','yun']
assert len(mylist)>=1
print mylist
mylist.pop()
mylist.pop()
mylist.append('heheda')
print mylist
assert len(mylist)>=1
