#!/usr/bin/python
#Filename:printMax.py
# print 'Hello World'
# i=5
# print i;
# i=i+1;print i;

# s='''This is a multi-line string.
# This is the second line.'''
# print s

# length=5
# breadth=2
# area=length*breadth
# print 'Aero is',area
# print 'Perimeter is',2*(length+breadth)

# #####if####
# number=23
# ########while
# running =True
# while running:
#     guess=int(raw_input('Enter an integer:'))
#     if guess==number:
#         print 'Congratulations, you guess it!.'
#         print "(but you do not win any prizes!)"
#         running=False
#     elif guess<number:
#         print 'No, it is a litter higher than that'
#     else:
#         print 'No, it is a litter lower than that'
# else:
#     print 'THe while loop is over'
# print 'Done'

# ####for
# for i in range(1,5):
#     print i
#     if i==3:
#         break
# else:
#     print 'The for loop is over'

# while True:
#     s=raw_input('Enter something:')
#     if s=='quit':
#         break
#     if len(s)<3:
#         continue
#     print 'Input is of sufficient length'
# print 'Done'

# def sayHello():
#     print 'Hello world!'
# sayHello()



# def printMax(a,b):
#     if a>b:
#         print a,'is maximum'
#     else:
#         print b,'is maximum'
# printMax(100,9)
# def func():
#     global x
#     print 'X is',x
#     x=2
#     print 'change local x to',x
# x=50
# func()
# print 'value of x is',x
# def say(message,times=1):
#     print message*times
# say('Hello')
# say('Hello',5)
# def keyfunc(a,b=5,c=10):
#     print 'a is',a,'and b is',b,'and c is',c
# keyfunc(3,7)
# keyfunc(25,c=19)
# keyfunc(c=100,a=50,b=21)

# def maximum(x,y):
#     if x>y:
#         return x
#     else:
#         return y
# print maximum(2,2)
#########Docstring##########
def printMax(x,y):
    '''Prints the maximum of two numbers.

The two values must be integers.'''
    x=int(x)
    y=int(y)
    if x>y:
        print x,'is maximum'
    else:
        print y,'is maximum'

print printMax(89,100)
print printMax.__doc__###
help(printMax)        
    


