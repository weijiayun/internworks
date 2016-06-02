
def log(text):
    if callable(text):
        @functools.wraps(text)
        def wrapper(*args,**kw):
            print 'begin call:{}'.format(text.__name__)
            text(*args,**kw)
            print 'end call:{}'.format(text.__name__)
        return wrapper
    else:
        def decrator(func):
            @functools.wraps(func)


            def wrapper(*args, **kw):
                print 'begin call:{}'.format(func.__name__)
                func(*args, **kw)
                print 'end call:{}'.format(func.__name__)
            return wrapper
        return decrator

def now():
    print 'hahhh'
now1=log('execute:')(now)
now1()
now2=log(now)
now2()

int('123456')
def char2num(s):
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,
            'B':11,'C':12,'D':13,'E':14,'F':15}[s]
print int('1A',16)



def strToInt(s,base=10):
    for ss in s:
        if ss in ('A','B','C','D','E','F'):
            base=16
    def fjin(x, y):
        return x * base + y
    return reduce(fjin,map(char2num,s))
print strToInt('1F')

def int2(x,base=2):
    return int(x,base)
import functools
int2new=functools.partial(int,base=2)
print int2new('111111')

max2=functools.partial(max,10)
print max2(5,6,7)

def mymax(*args):
    for index,item in enumerate(args):
        if index!=len(args)-1:
            if args[index]>args[index+1]:
                temp=args[index+1]
                args[index+1]=args[index]
                args[index]=temp
    return args[0][-1]

print mymax([100,3,4,3,6,8])
