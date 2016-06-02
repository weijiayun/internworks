#taskmanager
import random, time, Queue
import threading
from multiprocessing import Process
from multiprocessing.managers import BaseManager
class Student(object):
    def __init__(self,name=''):
        self.name=name

##queue of send task
task_queue=Queue.Queue()
##queue of receive task
result_queue=Queue.Queue()

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue',callable=lambda:task_queue)

QueueManager.register('get_result_queue',callable=lambda:result_queue)

manager=QueueManager(address=('',5000),authkey='abc')
manager.start()
task=manager.get_task_queue()
result=manager.get_result_queue()
TL=threading.local()
def process_thread():
    for i in range(5):
        TL.student=result.get(timeout=10)
        print('Result:{} in {}'.format(TL.student.name,threading.current_thread().name))

for i in range(10):
    name=str(random.randint(0,10000))
    student=Student(name)
    print('put task {}'.format(student.name))
    task.put(student)
print('Try get result...')
t1=Process(target=process_thread,name='thread_Hello')
t2=Process(target=process_thread,name='thread_world')
t1.start()
t2.start()
t1.join()
t2.join()
manager.shutdown()

