listgrid=[570 ,201 ,188,
          455 ,201 ,562,
          462 ,201 ,80,
          309 ,201 ,629,
          313 ,201 ,622,
          87  ,201 ,306,
          139 ,201 ,1393
          ]
def cal(core,limit,listg):
    for i in range(50,100,1):
        a=1
        sum1=0
        for j,e in enumerate(listg):
            if e/i==0:
                a*=1
            else:
                a*=e//i
            if (j+1)%3==0:
                sum1+=a
                a=1
        if sum1<core+limit:
            print sum1,i
cal(512,96,listgrid)
print [ e/67 for e in listgrid]

param="$(A,B,C,E,F)"
param= param.strip().split('$')
param = param[1].split(',')
param[0] = param[0][1:]
param[-1] = param[-1][:-1]

print param[-1]

