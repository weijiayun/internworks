def namedtple(name,args):
    def __init__(self,*argv):
        targv=[]
        for i in argv:
            targv.append(i)
        for key,value in zip(args,targv):
            self.__dict__[key]=value
    return type(name,(object,),dict(__init__=__init__))

Point=namedtple('Point',['x','y'])
p=Point(1,2)

print p.x
