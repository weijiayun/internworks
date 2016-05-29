import win32process,sched,time,os,sys,datetime
def RunExe(exePath):
    assert os.path.exists(exePath)
    exeFileDir = os.path.dirname(exePath)
    handle0 = win32process.CreateProcess(exeFilePath,
                                         '',
                                         None,
                                         None,
                                         0,
                                         win32process.CREATE_NO_WINDOW,
                                         None,
                                         exeFileDir,
                                         win32process.STARTUPINFO())

    return handle0[0]
def stopExe(processObj):
    win32process.TerminateProcess(processObj, 0)

def schedule_stop(processObj,inc):
    schedule=sched.scheduler(time.time,time.sleep)
    schedule.enter(inc,0,stopExe,(processObj,))
    schedule.run()

def strtime2Secs(strtime):
    t = datetime.datetime.now()
    ymd=t.strftime("%Y-%m-%d")
    strtime=ymd+"-"+strtime
    d=datetime.datetime.strptime(strtime,'%Y-%m-%d-%H:%M:%S')
    time_sec_float=time.mktime(d.timetuple())
    t = datetime.datetime.now()
    today_sec_float=time.mktime(t.timetuple())
    time_sec_int=int(time_sec_float)-int(today_sec_float)
    if time_sec_int<=0:
        raise Exception("Error:The deadline setting is before the currentime!!!")
    return time_sec_int

def Main(exePath,deadline):
    try:
        ProcessObj = RunExe(exePath)
        schedule_stop(ProcessObj, strtime2Secs(deadline))
        print "The job will end at the {}".format(deadline)
    except Exception, e:
        print e.message

if __name__=='__main__':
    exeFilePath =sys.argv[1]#"C:\\windows\\notepad.exe"#
    expire_time=sys.argv[2]#'20:41:10'
    Main(exeFilePath,expire_time)




