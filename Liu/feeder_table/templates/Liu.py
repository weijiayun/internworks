from copy import deepcopy
import os


def InstrumentToCsv(filePath,csvPath):
    assert os.path.exists(filePath)
    TableFirstline = ['M_CODE', 'A_CODE', 'B_CODE', 'INDEX_CODE', 'CPN_FORMULA',
                      'UP_THRESHOLD','DOWN_THRESHOLD', 'A_RATIO', 'THIS_COUPON',
                      'NEXT_COUPON', 'NEXT_RESET_DATE','A_ESTY_NAV', 'FUND_STATUS',
                      'FUND_STEP', 'POSITION_LEVEL', 'A_PRE_CLOSE','A_PRE_AMT',
                      'A_PRE_NAV', 'B_PRE_CLOSE', 'B_PRE_AMT', 'B_PRE_NAV',
                      'M_PRE_CLOSE','M_PRE_AMT', 'M_PRE_NAV', 'INDEX_PRE_CLOSE']
    f=open(filePath,'r')
    rawList=f.readlines()
    f.close()
    InstrusDict={}
    InstrusList=[]
    sectionlog=[]
    newrawList=[]
    for line in rawList:
        line=line.strip().strip('\n')
        if line[-1]==',':
            line=line[0:-1]
        newrawList.append(line)
    for i,e in enumerate(rawList):
        e=e.strip()
        if e=='{':
            n1=i
            continue
        elif "}" in e:
            sectionlog.append([n1+1, i])
    for e in sectionlog:
       InstrusList.append(newrawList[e[0]:e[1]])
    for i, group in enumerate(InstrusList):
        temp={}
        for j,e in enumerate(group):
            if ":" not in e:
                continue
            A=e.split(":")
            if A[1].strip() == "[":
                temp[A[0].strip().replace('"','')]=A[1].strip()+group[j+1]+group[j+2]
                continue
            temp[A[0].strip().replace('"','')]=A[1].strip().replace('"','')
        InstrusDict[temp['Id']]=temp

    FundLBIDict=deepcopy(InstrusDict)
    StructuredFundDict=deepcopy(InstrusDict)
    for e,value in InstrusDict.items():
        if value['InstrumentType']!='StructuredFund1':
            StructuredFundDict.pop(e)
            continue
        elif value['InstrumentType']=='StructuredFund1':
            FundLBIDict.pop(e)
            continue
        else:
            continue
    totalDict={}
    for key,s in StructuredFundDict.items():
        totalDict[key]={
            'INDEX_CODE':FundLBIDict[s['Index']]['FeedCode'],
            'CPN_FORMULA':s['CouponFormula'],
            'UP_THRESHOLD':s['UpThreshold'],
            'DOWN_THRESHOLD':s['DownThreshold'],
            'A_RATIO':s['ARatio'],
            'THIS_COUPON':s['ThisCoupon'],
            'NEXT_COUPON':s['NextCoupon'],
            'NEXT_RESET_DATE':s['NextResetDate'],
            'FUND_STATUS':s['Status'],
            'FUND_STEP':s['Step'],
            'POSITION_LEVEL':s['PositionLevel'],
            'A_ESTY_NAV':FundLBIDict[s['A']]['EstyNav'],
            'A_PRE_AMT':FundLBIDict[s['A']]['PreAmount'],
            'A_PRE_NAV':FundLBIDict[s['A']]['PreNav'],
            'A_PRE_CLOSE': "",
            'A_CODE': FundLBIDict[s['A']]['FeedCode'],
            'B_PRE_AMT':FundLBIDict[s['B']]['PreAmount'],
            'B_PRE_NAV':FundLBIDict[s['B']]['PreNav'],
            'B_CODE':FundLBIDict[s['B']]['FeedCode'],
            'B_PRE_CLOSE':"",
            'M_PRE_AMT':FundLBIDict[s['Base']]['PreAmount'],
            'M_PRE_NAV':FundLBIDict[s['Base']]['PreNav'],
            'M_CODE': FundLBIDict[s['Base']]['FeedCode'],
            'M_PRE_CLOSE':"",
            'INDEX_PRE_CLOSE':"",
            }
    if not os.path.exists(feederTableCsvPath):
        os.mkdir(os.path.split(feederTableCsvPath)[0])
    print "Writing {}".format(feederTableCsvPath)
    f=open(feederTableCsvPath,'w')

    for i,e in enumerate(TableFirstline):
        if i==len(TableFirstline)-1:
            f.write(e+'\n')
        else:
            f.write(e+',')
    for key, value in totalDict.items():
        for i,e in enumerate(TableFirstline):
            if i==len(value)-1:
                f.write(value[e]+'\n')
            else:
                f.write(value[e]+',')
    f.close()

if __name__=="__main__":
    instrufilepath = '/home/weijiayun/PycharmProjects/feeder_table/templates/Fund.instrument'
    feederTableCsvPath='/home/weijiayun/PycharmProjects/feeder_table/csvfiles/feederTable.csv'
    InstrumentToCsv(instrufilepath,feederTableCsvPath)
