import sched,time,os,sys,datetime
from multiprocessing import Process
def cmdread(exepath):
    exename=os.path.basename(exepath)
    os.execl(exepath,exename)

def RunExe(exePath,deadline):
    try:
        p1 = Process(target=cmdread,args=(exePath,))
        seconds = strtime2Secs(deadline)
        p1.start()
        p2 = Process(target=schedule_stop, args=(p1,seconds))
        p2.start()
        p2.join()
    except Exception, e:
        print e.message
def stopExe(processObj):
    processObj.terminate()

def schedule_stop(processObj,inc):
    schedule = sched.scheduler(time.time,time.sleep)
    schedule.enter(inc,0,stopExe,(processObj,))
    schedule.run()

def strtime2Secs(strtime):
    t = datetime.datetime.now()
    ymd = t.strftime("%Y-%m-%d")
    strtime = ymd+"-"+strtime
    d=datetime.datetime.strptime(strtime,'%Y-%m-%d-%H:%M:%S')
    time_sec_float = time.mktime(d.timetuple())
    t = datetime.datetime.now()
    today_sec_float = time.mktime(t.timetuple())
    time_sec_int = int(time_sec_float)-int(today_sec_float)
    if time_sec_int <= 0:
        raise Exception("Error:The deadline setting is before the currentime!!!")
    return time_sec_int

if __name__ == '__main__':
    exeFilePath = sys.argv[1]
    expire_time = sys.argv[2]
    print "The job will end at the {}".format(expire_time)
    RunExe(exeFilePath,expire_time)


