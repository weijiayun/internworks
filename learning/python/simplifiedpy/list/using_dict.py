#!/usr/bin/python
#Filename:using_dict.py

#'ab' id short for 'a' address'b'ook
ab={'Swaroop':'swaroop@mail.com',
    'Larry':'larry@wall.org',
    'Mat':'mat@info.com',
    'spam':'spam@hotmail.com'}
print "Swaroop's address is %s"%ab['Swaroop']

#Adding a key/value pair
ab['Guido']='guido@python.com'
#no order
#Deleting a key/value pair
del ab['spam']

print '\nThere are %d contacts in the address-book\n'%len(ab)
for name,address in ab.items():
    print 'Contact %s at %s'%(name,address)

if ab.has_key('Guido'):
    print "\nGuido's address is %s"%ab['Guido']
    
