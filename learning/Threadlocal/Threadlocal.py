import threading
class Student(object):
    def __init__(self,name):
        self.name=name
# globals_dict={}
# def process_thread(name):
#     '''process of student'''
#     std=Student(name)
#     globals_dict[threading.current_thread()]=std
#     process_student()
# def process_student():
#     print('Hello, {} (in {})\n'.format(globals_dict[threading.current_thread()].name,threading.current_thread().name))

local_school=threading.local()

def process_student():
    print('Hello, {} (in {})'.format(local_school.student,threading.current_thread().name))

def process_thread(name):
    local_school.student=name
    process_student()

t1=threading.Thread(target=process_thread,args=('Alice',),name='Thread-a')
t2=threading.Thread(target=process_thread,args=('bob',),name='Thread-b')
t1.start()
t2.start()
t1.join()
t2.join()
