#!/usr/bin/env python
#Filename:pacelem.py

'''a test module'''
__author__='Jiayun.Wei'
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import sys


def test():
    args=sys.argv
    if len(args)==1:
        print 'hello world!'
    elif len(args)==2:
        print 'hello,%s!'%args[1]
    else:
        print 'Too many arguments'

def _private_1(name):
    return 'Hello,%s'%name
def _private_2(name):
    return 'H1,%s'%name
def greeting(name):
    if len(name)>3:
        return _private_1(name)
    else:
        return _private_2(name)

print '\'xxx\' is unicode?',isinstance('xxx',unicode)
print 'u\'xxx\' is unicode',isinstance(u'xxx',unicode)
print '\'xxx\' is str?',isinstance('xxx',str)
print 'b\'xxx\' is str?',isinstance(b'xxx',str)
print 10/3
print 10.0/3


class Student(object):
    def __init__(self,name):
        self.__name=name
        #self.__score=score

    def printscore(self):
        print '{0}: {1}'.format(self.__name,self.__score)
    def get_name(self):
        return self.__name
    def get_score(self):
        return self.__score
    def setscore(self,score):
        if 0<=score<=100:
            self.__score=score
        else:
            raise ValueError('bad score')
    def __getattr__(self, item):
        if item=='score':
            return lambda:99
        if item=='age':
            return lambda:25
        raise AttributeError('\'Student\' object has no attribute \'%s\''%item)
    def __call__(self):
        print('my name is {}'.format(self.__name))

s=Student('weijiayun')
s()



class Chain(object):
    def __init__(self,path='http://www.sjtu.edu.cn'):
        self.path=path
    def __getattr__(self, path):
        return Chain('{}/{}'.format(self.path,path))
    def __str__(self):
        return  self.path
    __repr__=__str__
s=Chain('http://sjtu.edu.cn').login
print(s)




class Fib(object):
    def __init__(self):
        self.a,self.b=0,1
    def __iter__(self):
        return self
    def next(self):
        self.a,self.b=self.b,self.a+self.b
        if self.a>100000:
            raise StopIteration()
        return self.a
    def __getitem__(self, n):
        if isinstance(n,int):
            a,b=1,1
            for x in range(n):
                a,b=b,a+b
            return a
        elif isinstance(n,slice):
            start=n.start
            stop=n.stop
            step=n.step
            if start is None:
                start=0
            if step is None:
                step=1
            a,b=1,1
            L=[]
            for x in range(stop):
                if x>=start and x%step==0:
                    L.append(a)
                a,b=b,a+b
            return L
import logging
def functry(x,y):
    try:
        print('try...')
        r=x/y
        print('result:', r)
        return r
    # except ZeroDivisionError as e:
    #     print('except',e)
    # except ValueError as e:
    #     print('except',e)
    except Exception as e:
        logging.exception(e)
print(functry(10,'a'))

class FooErro(ValueError):
    pass

def foo(s):
    n=int(s)
    if n==0:
        raise FooErro("invalid value: {}".format(s))
    return 10/n

foo('0')


























if __name__=='__main__':
    pass











