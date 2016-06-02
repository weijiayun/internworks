#taskworker

import time,sys,Queue
#from taskmanager import Student
from multiprocessing.managers import BaseManager
class Student(object):
    def __init__(self,name=''):
        self.name=name
class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
server_addr='127.0.0.1'
print('Connect to sever {}...'.format(server_addr))
m=QueueManager(address=(server_addr,5000),authkey='abc')
m.connect()
task=m.get_task_queue()
result=m.get_result_queue()
#deal the data in this process
for i in range(10):
    try:
        student=task.get(timeout=10)
        print('run task Student:{}'.format(student.name))
        #r='{}'.format(student)
        r=student
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty')

print('worker exit.')