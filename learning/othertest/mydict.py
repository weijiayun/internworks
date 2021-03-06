class Dict(dict):
    '''
    Simple dict but also access as x.y style
    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self,**kwargs):
        super(Dict,self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute {}".format(item))

    def __setattr__(self, key, value):
        self[key]=value

if __name__=='__main__':
    import doctest
    doctest.testmod()
    # d=Dict(a=1,b=3)
    # print(d.a)
    # print(d['a'])


