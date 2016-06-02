# try:
#     f=open('test.txt','r')
#     print(f.read())
# finally:
#     if f:
#         f.close()
# with open('test.txt','r') as f:
#     for line in f.readlines():
#         print(line.strip())
import os

def search(s,dir='.'):
    for x1 in os.listdir(dir):
        try:
            x1=os.path.join(dir,x1)
            if os.path.isfile(x1):
                if s in os.path.split(x1)[1]:
                    print(x1)
            if os.path.isdir(x1):
                search(s,x1)
        except OSError:
            continue
search('maytheforce','/home/weijiayun/')







