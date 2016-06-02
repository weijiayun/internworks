import json

class Student(object):
    def __init__(self,name,age,score):
        self.name=name
        self.age=age
        self.score=score

def student2dict(std):
    return {
        'name':std.name,
        'age':std.age,
        'score':std.score
    }
def dict2student(std):
    return Student(std['name'],std['age'],std['score'])

f=open('json.txt','wb')
s=Student('weijiayun',24,88)
json.dump(student2dict(s),f)
f.close()
f=open('json.txt','rb')
line=f.readline()
print(json.loads(line,object_hook=dict2student))

if __name__=='__main__':
    pass