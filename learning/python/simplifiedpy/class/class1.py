#!/usr/bin/python
#Filename:class1.py

class Person:
    population=0#static member
    __privatevar 
    def __init__(self,name):
        self.name=name#in-class member
        Person.population+=1

    def __del__(self):
        '''I am dying.'''
        print '%s says bye.'%self.name
        Person.population-=1
        if Person.population==0:
            print 'I am the last one.'
        else:
            print 'There are still %d people left'%Person.population
    def sayHi(self):
        print "Hello, my name is",self.name
    def howMany(self):
        "Print the current population"
        if Person.population==1:
            print 'I am the only person here'
        else:
            print 'We have %d person here.'%Person.population


            
swaroop=Person('Swaroop')
swaroop.sayHi()
swaroop.howMany()

kalam=Person('Kalam')
kalam.sayHi()
kalam.howMany()

swaroop.sayHi()
swaroop.howMany()

