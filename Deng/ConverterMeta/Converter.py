__author__ = 'jiayun.wei'

import sys
import os
import copy,re
def StructureNameNotMatchError(filename):
    raise Exception('The template "{}.h.tmpl" Cannot MATCH Its Own Structure\'s Name'.format(filename))

def excludeMember(memberList,excludename):
    if excludename is not None:
        if not isinstance(excludename,list):
            excludename=list([excludename])
        for e in excludename:
            if e in memberList:
                excludenameIndex=memberList.index(e)
                del memberList[excludenameIndex]

def outfilecsv(memeblist,name,path):
    if not os.path.exists(path):
        os.mkdir(path)
    filename=os.path.join(path,name+'.csv')
    f=open(filename,'w')
    for i,m in enumerate(memeblist):
        if i==len(memeblist)-1:
            f.write("{}".format(m))
        else:
            f.write("{},".format(m))
    f.close()

def TypeExpand(optionList,typeList,memberList,initvars,typename,ElemNameSuffix,expandNum=1):
        for typeElem in typename:
            if typeElem in typeList:
                typeIndex=typeList.index(typeElem)
                tempmemberName=memberList[typeIndex]
                initvalue=initvars[typeIndex]
                option=optionList[typeIndex]
                del memberList[typeIndex]
                del typeList[typeIndex]
                del initvars[typeIndex]
                del optionList[typeIndex]
                ElemNameSuffix.reverse()
                for nameSuffix in ElemNameSuffix:
                    if nameSuffix[0] in typeElem:
                        for i in range(expandNum,0,-1):
                            for s in nameSuffix:
                                memberList.insert(typeIndex,tempmemberName+'_'+s+str(i))
                                typeList.insert(typeIndex,typeElem)
                                initvars.insert(typeIndex,initvalue)
                                optionList.insert(typeIndex,option)

def kwExpand(optionList,typeList,memberList,initvars,ElemNameSuffix,keyword,expandNum=1,iskeywords=True):
    if keyword in memberList:
        typeIndex=memberList.index(keyword)
        tempTypeName=typeList[typeIndex]
        initvalues=initvars[typeIndex]
        option=optionList[typeIndex]
        del memberList[typeIndex]
        del typeList[typeIndex]
        del initvars[typeIndex]
        del optionList[typeIndex]
        ElemNameSuffix.reverse()
        for i in range(expandNum,0,-1):
            for s in ElemNameSuffix:
                if iskeywords:
                    memberList.insert(typeIndex,keyword+'_'+s+str(i))
                else:
                    memberList.insert(typeIndex,s+str(i))
                typeList.insert(typeIndex,tempTypeName)
                initvars.insert(typeIndex,initvalues)
                optionList.insert(typeIndex,option)

def findAllList(Path):
    f=open(Path)
    name =os.path.basename(Path)
    name= name.split('.')[0]
    lns = f.readlines()
    f.close()
    npos1=-1
    npos2=0
    method=""
    for line in lns:
        npos1+=1
        if name in line:
            if '(Strategy:' in line:
                method='Strategy'
            elif '(Signal:' in line:
                method='Signal'
            npos1+=2
            break
    for i in range(npos1,len(lns)):
        if '};' in lns[i]:
            npos2=i
            break
    temTotalList=[]
    for i in range(npos1,npos2):
        elemrow=lns[i].strip()
        if elemrow=='':
            continue
        if elemrow[-1]==';':
            elemrow= elemrow[:-1]
        elemlist=elemrow.strip().split(' ')
        if elemlist[2]=='Id' or elemlist[2]=='Description':
            continue
        temTotalList.append(elemlist)
    TotalList=[]
    for e in temTotalList:
        if len(e)>4:
            if e[-2]=='reference':
                TotalList.append(dict(option=e[0],type=e[1],varname=e[2],Reference=e[-1],Default=""))
                continue
            elif e[-2]=='default'or e[-2]=='equal':
                TotalList.append(dict(option=e[0],type=e[1],varname=e[2],Reference="",Default=e[-1]))
                continue
        else:
            TotalList.append(dict(option=e[0],type=e[1],varname=e[2],Reference="",Default=""))
            continue
    if TotalList==[]:
        StructureNameNotMatchError(name)
    return [name,TotalList,method]

def dollarFuncCheck(memberlist,initVars):
    funcDict={memberlist[i]:e for i,e in enumerate(initVars) if '$'in e}
    for i,e in enumerate(initVars):
        if '$' in e:
            initVars[i] = ""
    dollarCheckResultsDict = {}
    for key,value in funcDict.items():
        if '$$' in value:
            dollarsplit = value.split('$$')
            twoDollardigitList= [0 for c in dollarsplit[1:]]
            dollar1split=dollarsplit[0]
            dollarsplit=  dollar1split.split('$')
            funcName = value.split('$')[1][:-1]
            if dollarsplit[2:][0]=='None,':
                oneDollarList=[0 for c in dollarsplit[2:]]
            else:
                oneDollarList = [1 for c in dollarsplit[2:]]

            oneDollarList[len(oneDollarList):len(oneDollarList)]=twoDollardigitList
            extendElems=oneDollarList
        else:
            dollarsplit = value.split('$')
            funcName = value.split('$')[1][:-1]
            if dollarsplit[2:][0]=='None)':
                extendElems = [0 for c in dollarsplit[2:]]
            else:
                extendElems = [1 for c in dollarsplit[2:]]
        oneDollarStrList = [c[:-1]for c in dollarsplit[2:]]
        dollarCheckResultsDict[key]=[funcName,oneDollarStrList,extendElems]
    return dollarCheckResultsDict
#################################################################################################

def GenerateSignalPythonScript(SignalList,desPath,csvpath,excludelist):
    AllList=SignalList[1]
    name=SignalList[0]
    optionList = []
    TypeList=[]
    Memberlist=[]
    initVar=[]
    boolList=[]
    for e in AllList:
        TypeList.append(e['type'])
        Memberlist.append(e['varname'])
        initVar.append(e['Default'])
        optionList.append(e['option'])

####################Type,Name,sort in the first###############
    if 'Type' in Memberlist:
        NameIndex=Memberlist.index('Type')
        Memberlist.insert(0,Memberlist[NameIndex])
        del Memberlist[NameIndex+1]
        TypeList.insert(0,TypeList[NameIndex])
        del TypeList[NameIndex+1]
        initVar.insert(0,initVar[NameIndex])
        del initVar[NameIndex+1]
        optionList.insert(0, optionList[NameIndex])
        del optionList[NameIndex + 1]

    if 'Name' in Memberlist:
        NameIndex=Memberlist.index('Name')
        Memberlist.insert(0,Memberlist[NameIndex])
        del Memberlist[NameIndex+1]
        TypeList.insert(0,TypeList[NameIndex])
        del TypeList[NameIndex+1]
        initVar.insert(0,initVar[NameIndex])
        del initVar[NameIndex+1]
        optionList.insert(0, optionList[NameIndex])
        del optionList[NameIndex + 1]

    signalfuncdict=dollarFuncCheck(Memberlist,initVar)

    waitForMemberlist=copy.deepcopy(Memberlist)

####################job to expand types#######################
    expandtype=['list<OrderByNominal>','list<OrderByVolume>']
    nameSuffix1=[['Nominal','Type'],['Volume','Type']]
    TypeExpand(optionList,TypeList,Memberlist,initVar,expandtype,nameSuffix1,2)
    nameSuffix2=['InstrumentName','IsConnect','Market']
    kwExpand(optionList,TypeList,Memberlist,initVar,nameSuffix2,'Instruments',1)
    nameSuffix3=['Action','START','END']
    kwExpand(optionList,TypeList,Memberlist,initVar,nameSuffix3,'Ranges',1,False)

    if not os.path.exists(desPath):
        os.mkdir(desPath)
    f2=open('{}Converter.py'.format(os.path.join(desPath,name)),'w+')

    import1='import json,re'
    import2='from MiniMOManager.common.Util import is_bool,OrderedObject'
    import3='from MiniMOManager.common.SignalManager import SignalObject, SignalFinder'
    import4='from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name'
    import5='from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager'
    importlist=[import1,import2,import3,import4,import5]

    for elemt in importlist:
        f2.write('{}\n'.format(elemt))
    f2.write('\nclass {0}Meta(OrderedObject):\n\040\040\040\040def __init__(self):\n\040\040\040\040\040\040\040\040super({0}Meta,self).__init__()\n'.format(name))
#######CSV#################################################
    outfilecsv(Memberlist,name,csvpath)
######initialize the vars in the list######################
    for index,ivalue in enumerate(initVar):
        if ivalue =='""' or ivalue=="''":
            f2.write('\040\040\040\040\040\040\040\040self.{0} = ""\n'.format(Memberlist[index]))
            continue
        elif str.lower(ivalue)=='true' or str.lower(ivalue)=='false':
            f2.write("\040\040\040\040\040\040\040\040self.{0} = {1}\n".format(Memberlist[index]
                     ,str.upper(ivalue)[0]+str.lower(ivalue)[1:]))
            continue
        elif re.match(r'[0-9]+',ivalue):
            f2.write('''\040\040\040\040\040\040\040\040self.{0} = {1}\n'''.format(Memberlist[index],ivalue))
            continue
        elif isinstance(ivalue,str):
            f2.write('''\040\040\040\040\040\040\040\040self.{0} = "{1}"\n'''.format(Memberlist[index],ivalue))
            continue
    f2.write('\n\040\040\040\040def get_const_member_list(self):\n\040\040\040\040\040\040\040\040member_list = [')

    excludeMember(waitForMemberlist,excludelist)
    for i in range(0,len(waitForMemberlist)):
        if i==len(waitForMemberlist)-1:
            f2.write("'{}']".format(waitForMemberlist[i]))
            break
        f2.write("'{}',".format(waitForMemberlist[i]))
        if i%3==0 and i!=0:
            f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040')
    f2.write('\n\040\040\040\040\040\040\040\040return member_list')

    signalvarslist = [Memberlist[i] for i, var in enumerate(TypeList) if var == "signal"]
    f2.write('\n\n\040\040\040\040def get_signal_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040signal_list = {}'.format(signalvarslist))
    f2.write('\n\040\040\040\040\040\040\040\040return signal_list')

    required_member_list=[Memberlist[i] for i,var in enumerate(optionList) if var == "required"]
    f2.write('\n\n\040\040\040\040def required_member_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040required_list={}'.format(required_member_list))
    f2.write('\n\040\040\040\040\040\040\040\040return required_list')

    optional_member_list = [Memberlist[i] for i, var in enumerate(optionList) if var == "optional"]
    f2.write('\n\n\040\040\040\040def optional_member_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040optional_list={}'.format(optional_member_list))
    f2.write('\n\040\040\040\040\040\040\040\040return optional_list')

    # if len(signalfuncdict) != 0:
    #     f2.write('\n\n\040\040\040\040def get_function_dict(self):')
    #     f2.write('\n\040\040\040\040\040\040\040\040function_dict = {}'.format(signalfuncdict))
    #     f2.write('\n\040\040\040\040\040\040\040\040return function_dict')

    boolList = [Memberlist[i] for i, var in enumerate(TypeList) if var == "bool"]
    f2.write('\n\n\040\040\040\040def get_bool_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040bool_list = {0}'.format(boolList))
    f2.write('\n\040\040\040\040\040\040\040\040return bool_list')
    f2.write('\n\nclass {}Converter(object):'.format(name))
    f2.write('\n\n\040\040\040\040def __init__(self):')
    f2.write('\n\040\040\040\040\040\040\040\040self.__{}_meta_list = []'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040self.__signal_object_list = []')

    f2.write('\n\n\040\040\040\040def set_meat_list(self, {0}_meta_list):'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040self.__{0}_meta_list = {0}_meta_list'.format(name))

    f2.write('\n\n\040\040\040\040def start_converter(self):')
    f2.write('\n\040\040\040\040\040\040\040\040for meta in self.__{0}_meta_list:'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040self.strategy_to_json(meta)')
    f2.write('\n\040\040\040\040\040\040\040\040return self.__signal_object_list')

    f2.write('\n\n\040\040\040\040def strategy_to_json(self, {0}Meta):'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040data_json = {}')
    f2.write('\n\040\040\040\040\040\040\040\040try:')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040signal_finder = SignalFinder()')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040is_error = False')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040for member in {0}Meta.get_const_member_list():'.format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040member_value = getattr({0}Meta, member)".format(name))
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040if member in {0}Meta.get_bool_list():'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = is_bool(getattr({0}Meta, member))'.format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040elif member in {0}Meta.get_signal_list():\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040if data_json[member] == -1:")
    f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040is_error=True''')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040else:')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = getattr({0}Meta, member)'.format(name))

    if len(signalfuncdict) != 0:
        for key,value in signalfuncdict.items():
            param1 = ""
            param2=""
            a=len(value[2])-len(value[1])
            for i in range(len(value[2])):
                if i != len(value[2])-1:
                    param1 += '{%s},'%i
                else:
                    param1 += '{%s}'%i
            for i, its in enumerate(value[1]):
                if its != 'None' and its != 'none':
                    if i == len(value[1]) - 1:
                        param2 += "{}Meta.".format(name) + its
                    else:
                        param2 += "{}Meta.".format(name) + its + ','
                else:
                    param2 = 'None'
            if a != 0:
                param3 = ""
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param = data_json["{}"].strip().split('$')'''.format(key))
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param = param[1].split(',')''')
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param[0] = param[0][1:]''')
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param[-1] = param[-1][:-1]''')
                if len(value[2]) != 0:
                    for i in range(-a,0,1):
                        if len(value[1]) == 0:
                            if i == -1:
                                param3 += "param[{}]".format(i)
                            else:
                                param3 += "param[{}],".format(i)
                        else:
                            param3 += ",param[{}]".format(i)
                    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040data_json["{}"]'.format(key) + ' = reference_arg_manager("${}({})"'.format(value[0],param1) + '.format({}{}))'.format(param2,param3))
            else:
                f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040data_json["{}"]'.format(key) + ' = reference_arg_manager("${}({})"'.format(value[0], param1) + '.format({}))'.format(param2))



    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040if not is_error:')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040signal_object = SignalObject()')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040signal_object.name = {0}Meta.Name'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040signal_object.type = {0}Meta.Type'.format(name))
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040signal_object.enable = True')

    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040signal_object.node = json.dumps(data_json)')
    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040self.__signal_object_list.append(signal_object)')
    f2.write("\n\040\040\040\040\040\040\040\040except Exception as e:")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040raise CSVConverterError({0}Meta.Name, {0}Meta.Type, e.message)".format(name))

    f2.write('\n\n\040\040\040\040def get_signal_id(self, signal_id):')
    f2.write('\n\040\040\040\040\040\040\040\040signal_id_list = [signal_id]')
    f2.write('\n\040\040\040\040\040\040\040\040return signal_id_list')
    f2.close()
    


###############Strategy######################################################################################
def GenerateStrategyPythonScript(StrategyList, desPath,csvpath,excludelist=None):

    AllList=StrategyList[1]
    name=StrategyList[0]
    TypeList = []
    Memberlist = []
    initVar = []
    boolList = []
    optionList = []
    for e in AllList:
        TypeList.append(e['type'])
        Memberlist.append(e['varname'])
        initVar.append(e['Default'])
        optionList.append(e['option'])
    for i,bo in enumerate(TypeList):
        if bo == 'bool':
            boolList.append(Memberlist[i])
    if 'Type' in Memberlist:
        NameIndex=Memberlist.index('Type')
        Memberlist.insert(0,Memberlist[NameIndex])
        del Memberlist[NameIndex+1]
        TypeList.insert(0,TypeList[NameIndex])
        del TypeList[NameIndex+1]
        initVar.insert(0,initVar[NameIndex])
        del initVar[NameIndex+1]
        optionList.insert(0,optionList[NameIndex])
        del optionList[NameIndex+1]

    if 'Name' in Memberlist:
        NameIndex=Memberlist.index('Name')
        Memberlist.insert(0,Memberlist[NameIndex])
        del Memberlist[NameIndex+1]
        TypeList.insert(0,TypeList[NameIndex])
        del TypeList[NameIndex+1]
        initVar.insert(0,initVar[NameIndex])
        del initVar[NameIndex+1]
        optionList.insert(0, optionList[NameIndex])
        del optionList[NameIndex + 1]

    signalfuncdict = dollarFuncCheck(Memberlist, initVar)
    waitForMemberlist=copy.deepcopy(Memberlist)
    #######################get signal list########################
    signalvarslist = []
    for i,bo in enumerate(TypeList):
        if bo == 'signal':
            signalvarslist.append(Memberlist[i])
####################job to expand types########################

    expandtype=['list<OrderByNominal>','list<OrderByVolume>']
    nameSuffix1=[['Nominal','Type'],['Volume','Type']]
    TypeExpand(optionList,TypeList,Memberlist,initVar,expandtype,nameSuffix1,2)
    nameSuffix2=['InstrumentName','IsConnect','Market']
    kwExpand(optionList,TypeList,Memberlist,initVar,nameSuffix2,'Instruments',1)
    nameSuffix3=['Action','START','END']
    kwExpand(optionList,TypeList,Memberlist,initVar,nameSuffix3,'Ranges',1,False)

    if not os.path.exists(desPath):
        os.mkdir(desPath)
    f2=open('{}Converter.py'.format(os.path.join(desPath,name)),'w+')
    f2.write("__author__ = '{}'\n\n".format(__name__))
    import1='import json'
    import2='from MiniMOManager.common.BPManager import BPManager'
    import3='from MiniMOManager.common.SignalManager import SignalFinder'
    import4='from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name'
    import5='from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager'
    importlist=[import1,import2,import3,import4,import5]

    for elemt in importlist:
        f2.write('{}\n'.format(elemt))
    f2.write('\nclass {0}Meta(OrderedObject):\n\040\040\040\040def __init__(self):\n\040\040\040\040\040\040\040\040super({0}Meta,self).__init__()\n'.format(name))
#######CSV#################################################
    outfilecsv(Memberlist,name,csvpath)
######initialize the vars in the list######################
    for index,ivalue in enumerate(initVar):
        if ivalue =='""' or ivalue=="''":
            f2.write('\040\040\040\040\040\040\040\040self.{0} = ""\n'.format(Memberlist[index]))
            continue
        elif str.lower(ivalue)=='true' or str.lower(ivalue)=='false':
            f2.write("\040\040\040\040\040\040\040\040self.{0} = {1}\n".format(Memberlist[index]
                     ,str.upper(ivalue)[0]+str.lower(ivalue)[1:]))
            continue
        elif re.match(r'[0-9]+',ivalue):
            f2.write('''\040\040\040\040\040\040\040\040self.{0} = {1}\n'''.format(Memberlist[index],ivalue))
            continue
        elif isinstance(ivalue,str):
            f2.write('''\040\040\040\040\040\040\040\040self.{0} = "{1}"\n'''.format(Memberlist[index],ivalue))
            continue

    f2.write('\n\040\040\040\040def get_const_member_list(self):\n\040\040\040\040\040\040\040\040member_list = [')

    excludeMember(waitForMemberlist,excludelist)
    for i in range(0,len(waitForMemberlist)):
        if i==len(waitForMemberlist)-1:
            f2.write("'{}']".format(waitForMemberlist[i]))
            break
        f2.write("'{}',".format(waitForMemberlist[i]))
        if i%3==0 and i!=0:
            f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040')
    f2.write('\n\040\040\040\040\040\040\040\040return member_list')

    signalvarslist = [Memberlist[i] for i, var in enumerate(TypeList) if var == "signal"]
    f2.write('\n\n\040\040\040\040def get_signal_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040signal_list = {}'.format(signalvarslist))
    f2.write('\n\040\040\040\040\040\040\040\040return signal_list')

    required_member_list=[Memberlist[i] for i,var in enumerate(optionList) if var == "required"]
    f2.write('\n\n\040\040\040\040def required_member_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040required_list={}'.format(required_member_list))
    f2.write('\n\040\040\040\040\040\040\040\040return required_list')

    optional_member_list = [Memberlist[i] for i, var in enumerate(optionList) if var == "optional"]
    f2.write('\n\n\040\040\040\040def optional_member_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040optional_list={}'.format(optional_member_list))
    f2.write('\n\040\040\040\040\040\040\040\040return optional_list')

    boolList = [Memberlist[i] for i, var in enumerate(TypeList) if var == "bool"]
    f2.write('\n\n\040\040\040\040def get_bool_list(self):')
    f2.write('\n\040\040\040\040\040\040\040\040bool_list = {0}'.format(boolList))
    f2.write('\n\040\040\040\040\040\040\040\040return bool_list')

    f2.write('\n\n\040\040\040\040def get_strategy_csv_header(self):\n\040\040\040\040\040\040\040\040header_list = []\n\040\040\040\040\040\040\040\040for header in dir(self):'
             "\n\040\040\040\040\040\040\040\040\040\040\040\040if header[:2] != '__' and header[-2:] != '__' and header[:4] != 'get_':"
             "\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040header_list.append(header)\n\040\040\040\040\040\040\040\040return header_list")

    # if len(signalfuncdict) != 0:
    #     f2.write('\n\n\040\040\040\040def get_function_dict(self):')
    #     f2.write('\n\040\040\040\040\040\040\040\040function_dict = {}'.format(signalfuncdict))
    #     f2.write('\n\040\040\040\040\040\040\040\040return function_dict')

    f2.write("\n\n\040\040\040\040def get_portfolio_list(self):")
    f2.write("\n\040\040\040\040\040\040\040\040portfolio_list = ['Portfolio']")
    f2.write("\n\040\040\040\040\040\040\040\040return portfolio_list")

    f2.write("\n\n\040\040\040\040def get_MatchStrategyId(self):")
    f2.write("\n\040\040\040\040\040\040\040\040ID_list = ['MatchStrategyId']")
    f2.write("\n\040\040\040\040\040\040\040\040return ID_list\n")
    f2.write("\nclass {}Converter(object):\n\040\040\040\040".format(name))
    f2.write("def __init__(self, work_dir=None):\n\040\040\040\040\040\040\040\040self.id = float('nan')\n\040\040\040\040\040\040\040\040self.__{}_meta_list = []"
             "\n\040\040\040\040\040\040\040\040self.work_dir = work_dir\n\040\040\040\040\040\040\040\040self.__bp_manager = None\n\040\040\040\040\040\040\040\040\n".format(name))
    f2.write("\040\040\040\040def set_meat_list(self, HeFeiV3_meta_list):\n\040\040\040\040\040\040\040\040self.__{}_meta_list = HeFeiV3_meta_list\n\n".format(name))
    f2.write("\040\040\040\040def get_meat_list(self):\n\040\040\040\040\040\040\040\040return self.__{}_meta_list\n\n".format(name))
    f2.write("\040\040\040\040def init_bp_manager(self):\n\040\040\040\040\040\040\040\040if self.__bp_manager is None:\n\040\040\040\040\040\040\040\040\040\040\040\040self.__bp_manager = BPManager()\n\n")
    f2.write("\040\040\040\040def init_strategy_id(self):\n\040\040\040\040\040\040\040\040self.id = get_max_id(self.work_dir)\n\040\040\040\040\040\040\040\040if self.id == -1:\n\040\040\040\040\040\040\040\040\040\040\040\040"
             "self.id = self.__bp_manager.get_max_portfolio_id()\n\n")
    f2.write("\040\040\040\040def start_converter(self):\n\040\040\040\040\040\040\040\040self.init_bp_manager()\n\040\040\040\040\040\040\040\040self.init_strategy_id()\n\040\040\040\040\040\040\040\040"
             "for meta in self.__{0}_meta_list:\n\040\040\040\040\040\040\040\040\040\040\040\040self.strategy_to_json(meta)\n\n".format(name))

    f2.write("\040\040\040\040def strategy_to_json(self, {0}Meta):".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040data_json = {}\n\040\040\040\040\040\040\040\040try:\n\040\040\040\040\040\040\040\040\040\040\040\040signal_finder = SignalFinder()")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040for member in {0}Meta.get_const_member_list():\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040member_value = getattr({0}Meta, member)".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040if member in {0}Meta.get_portfolio_list():\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = reference_portfolio(member_value)\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040".format(name))
    f2.write('''if data_json[member] == -1:\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040raise CSVConverterError({0}Meta.Name, {0}Meta.Type, "Can't find portfolio: {1}'''.format(name,'''{0}".format(member_value))'''))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040elif member in {0}Meta.get_signal_list():\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040if data_json[member] == -1:")
    f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040raise CSVConverterError({0}Meta.Name, {0}Meta.Type, "Can't find signal: {1}\n'''.format(name,'''{0}".format(member_value))'''))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040elif member in {0}Meta.get_bool_list():".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = is_bool(member_value)")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040elif member in {0}Meta.get_MatchStrategyId():".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = (get_strategy_id_by_name(self.work_dir, member_value), member_value)[isinstance(member_value, int)]")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040if data_json[member] == -1:")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040raise CSVConverterError({0}Meta.Name, {0}Meta.Type,".format(name)+''' "Can't find matchstrategy:{0}".format(member_value))''')
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040else:\n\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040\040data_json[member] = member_value")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040data_json['Instruments'] = generate_instruments({0}Meta, {0}Meta.member_list)".format(name))
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040data_json['Ranges'] = generate_ranges({0}Meta, {0}Meta.member_list)".format(name))

    if len(signalfuncdict) != 0:
        for key, value in signalfuncdict.items():
            param1 = ""
            param2 = ""
            a = len(value[2]) - len(value[1])
            for i in range(len(value[2])):
                if i != len(value[2]) - 1:
                    param1 += '{%s},' % i
                else:
                    param1 += '{%s}' % i
            for i, its in enumerate(value[1]):
                if its != 'None' and its != 'none':
                    if i == len(value[1]) - 1:
                        param2 += "{}Meta.".format(name) + its
                    else:
                        param2 += "{}Meta.".format(name) + its + ','
                else:
                    param2 = 'None'
            if a != 0:
                param3 = ""
                f2.write(
                    '''\n\040\040\040\040\040\040\040\040\040\040\040\040param = data_json["{}"].strip().split('$')'''.format(
                        key))
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param = param[1].split(',')''')
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param[0] = param[0][1:]''')
                f2.write('''\n\040\040\040\040\040\040\040\040\040\040\040\040param[-1] = param[-1][:-1]''')
                if len(value[2]) != 0:
                    for i in range(-a, 0, 1):
                        if len(value[1]) == 0:
                            if i == -1:
                                param3 += "param[{}]".format(i)
                            else:
                                param3 += "param[{}],".format(i)
                        else:
                            param3 += ",param[{}]".format(i)
                    f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040data_json["{}"]'.format(
                        key) + ' = reference_arg_manager("${}({})"'.format(value[0], param1) + '.format({}{}))'.format(
                        param2, param3))
            else:
                f2.write('\n\040\040\040\040\040\040\040\040\040\040\040\040data_json["{}"]'.format(
                    key) + ' = reference_arg_manager("${}({})"'.format(value[0], param1) + '.format({}))'.format(
                    param2))


    f2.write("\n\040\040\040\040\040\040\040\040except Exception as e:")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040raise CSVConverterError({0}Meta.Name, {0}Meta.Type, e.message)".format(name))

    f2.write("\n\040\040\040\040\040\040\040\040if self.work_dir is not None:")
    f2.write("\n\040\040\040\040\040\040\040\040\040\040\040\040self.__create_file(data_json)")
    f2.write("\n\040\040\040\040\040\040\040\040return data_json")
    f2.write("\n\040\040\040\040def __create_file(self, data):\n\040\040\040\040\040\040\040\040self.id += 1\n\040\040\040\040\040\040\040\040data['Id'] = self.id\n\040\040\040\040\040\040\040\040"
             "file_path = '{0}/Existed_Json_Module/{1:0>4}{2}.strategy'."
             "format(self.work_dir, data['Id'], data['Name'])\n\040\040\040\040\040\040\040\040json.dump([data], open(file_path, 'w'))\n\040\040\040\040\040\040\040\040return self.id\n\n")
    f2.close()
def is_somefile(filepath,sufix):
    assert os.path.exists(filepath)
    if os.path.isfile(filepath):
        name=os.path.basename(filepath)
        index=name.index('.')+1
        namesufix=name[index:]
        return namesufix==sufix

def search(s,dir,outputList):
    for x1 in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,x1)):
            if s in x1:
                ndir=os.path.abspath(dir)
                outputList.append(os.path.join(ndir,x1))
        if os.path.isdir(os.path.join(dir,x1)):
            search(s,os.path.join(dir,x1),outputList)

#################################################################################################
def GeneratePythonScripts(templateFileOrdirPath,generatePyPath,CsvPath,strategyMethod=['Automaton','SizeStrategy'],signalMethod=None):
    excludeVarnames=['Ranges','Instruments']
    assert os.path.exists(templateFileOrdirPath)
    if os.path.isdir(templateFileOrdirPath):
        tmplfilelist=[]
        search('.h.tmpl',templateFileOrdirPath,tmplfilelist)
        for f in tmplfilelist:
            if is_somefile(f,'h.tmpl'):
                templateList=findAllList(f)
                if templateList[2]=='Strategy':
                    GenerateStrategyPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)
                    continue
                elif templateList[2]=='Signal':
                    GenerateSignalPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)
                    continue
                else:
                    if strategyMethod is None:
                        GenerateStrategyPythonScript(templateList, generatePyPath, CsvPath, excludeVarnames)
                        continue
                    else:
                        if templateList[0] in strategyMethod:
                            GenerateStrategyPythonScript(templateList, generatePyPath, CsvPath, excludeVarnames)
                            continue
            else:
                continue
    elif os.path.isfile(templateFileOrdirPath):
        templateList=findAllList(templateFileOrdirPath)
        if templateList[2]=='Strategy':
            GenerateStrategyPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)
        elif templateList[2]=='Signal':
            GenerateSignalPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)
        elif templateList[0] in strategyMethod:
            GenerateStrategyPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)
        elif templateList[0] in signalMethod:
                GenerateSignalPythonScript(templateList,generatePyPath,CsvPath,excludeVarnames)


if __name__=='__main__':
    filePath='./tmplfiles/'
    PythonPath='./converterPyFiles'
    csvPath='./csvfiles'
    strategyMethod=['Automaton','SizeStrategy']
    try:
        GeneratePythonScripts(filePath,PythonPath,csvPath,strategyMethod)
    except Exception,e:
        print e.message




