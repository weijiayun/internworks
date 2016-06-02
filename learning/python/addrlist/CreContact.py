#!/usr/bin/python
#Filename:CreContact.py
import Contactslist as Addr
filename='inContact.info'
NewContact=Addr.Contact()
f=file(filename)
while True:
    pieceinfo=f.readline()
    if len(pieceinfo)==0:
        break
    piecesplit=pieceinfo.split()
    name=piecesplit[0]
    email=piecesplit[1]
    phone=piecesplit[2]
    person=Addr.Memberinfo(name,email,phone)
    NewContact.addMember(person)
NewContact.sort(1)
NewContact.delMember('Linus')
NewContact.dispMembers()

NewContact.saveContacts('contactlist.info')

