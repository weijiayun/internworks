#multiprocessing.py

import os
from multiprocessing import Process
from multiprocessing import Pool,Queue
print('process ({}) start...'.format(os.getpid()))
pid=os.fork()
if pid==0:
    print('I am child process ({}) and my parent is {}'.format(os.getpid(),os.getppid()))
else:
    print('I ({}) just created a child process ({}).'.format(os.getpid(),pid))
#
import time,random
def run_proc(name):
    print('run the child process {0} ({1})'.format(name,os.getpid()))
def long_time_task(name):
    print('run tast {} ({})'.format(name,os.getpid()))
    start=time.time()
    time.sleep(random.random()*3)
    end=time.time()
    print('Tast %s tuns %0.2f seconds'%(name,end-start))
##################communication among different processes#########
#####write data processing#########
def write(q):
    for value in ['a','b','c']:
        print('put {} to queue...'.format(value))
        q.put(value)
        time.sleep(random.random())
#####read data processing#########
def read(q):
    while True:
        value=q.get(True)
        print('Get %s from queue'%value)



if __name__=='__main__':
    # print('Parent process {}'.format(os.getpid()))
    # p=Process(target=run_proc,args=('test',))
    # print('process will start.')
    # p.start()
    # p.join()
    # print('process end')
    # print('Parent process {}'.format(os.getpid()))
    # p=Pool()
    # for i in range(5):
    #     p.apply_async(long_time_task,args=(i,))
    # print('waiting for all subprocess done...')
    # p.close()
    # p.join()
    # print('All subprocesses done')
    #parent process create Queue, and transfer data to threads
    q=Queue()

    pw=Process(target=write,args=(q,))
    pr=Process(target=read,args=(q,))
    # start the thread pw,write
    pw.start()
    #start the thread pr,read
    pr.start()
    #waitting for the end of pw
    pw.join()
    #pr is infinite loop,we can't wait the end of it, so we have to force to terminate it
    pr.terminate()










