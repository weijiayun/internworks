#!/usr/bin/python
#Filename:using_tuple.py

zoo=['wolf','elephant','penguin']
print 'The number od animals in the zoo is',len(zoo)

new_zoo=('monkey','dolphin',zoo)
new_zoo[2].append('spider')
print 'Number od animals in the zoo is',len(new_zoo)

print 'All the animals in the zoo are',new_zoo
print 'Animals btought from old zoo are',new_zoo[2]
print 'Last animal brought from old zoo is',new_zoo[2][2]

age=22
name='Swaroop'
a=(name,age)
print '%s is %d years old'%a
print 'Why is %s playing with that python?'%name
