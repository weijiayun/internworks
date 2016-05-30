import json,re
from MiniMOManager.common.Util import is_bool,OrderedObject
from MiniMOManager.common.SignalManager import SignalObject, SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class SouthMeta(OrderedObject):
    def __init__(self):
        super(SouthMeta,self).__init__()
        self.Name=""
        self.Type="South"
        self.South=""
        self.BalanceDateSignal=""
        self.BalanceDate=""
        self.NeedSigalDataFromAthene=""
        self.Mode="Autonomy"

    def get_const_member_list(self):
        member_list = ['Name','Type','South','BalanceDateSignal',
            'BalanceDate','NeedSigalDataFromAthene','Mode']
        return member_list

    def get_signal_list(self):
        signal_list=['BalanceDateSignal']
        return signal_list

    def get_function_dict(self):
        function_dict={'South': ['GetSouth', [1, 0]]}
        return function_dict

    def get_bool_list(self):
        bool_list=['NeedSigalDataFromAthene']
        return bool_list

class SouthConverter(object):

    def __init__(self):
        self.__South_meta_list = []
        self.__signal_object_list = []

    def set_meat_list(self, South_meta_list):
        self.__South_meta_list = South_meta_list

    def start_converter(self):
        for meta in self.__South_meta_list:
            self.strategy_to_json(meta)
        return self.__signal_object_list

    def strategy_to_json(self, SouthMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            is_error = False
            for member in SouthMeta.get_const_member_list():
                member_value = getattr(SouthMeta, member)
                if member in SouthMeta.get_bool_list():
                    data_json[member] = is_bool(getattr(SouthMeta, member))
                elif member in SouthMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        is_error=True
                else:
                    data_json[member] = getattr(SouthMeta, member)
            for key,value in SouthMeta.get_function_dict():
                param = re.split(r'[\(\)]+',data_json[key].strip())
                param = re.split(r',',param[1].strip())
                for i,e in enumerate(value[1]):
                    if e == 1:
                        param[i] = "SouthMeta."+param[i]
                temp = ""
                for i,e in enumerate(param):
                    if i == len(param)-1:
                        temp += e
                    else:
                        temp += e + ","
                FuncAndName = "${}({})".format(value[0],temp)
                data_json["{}".format(value[0])] = reference_arg_manager("{}".format(FuncAndName))
            if not is_error:
                signal_object = SignalObject()
                signal_object.name = SouthMeta.Name
                signal_object.type = SouthMeta.Type
                signal_object.enable = True
                signal_object.node = json.dumps(data_json)
                self.__signal_object_list.append(signal_object)
        except Exception as e:
            raise CSVConverterError(SouthMeta.Name, SouthMeta.Type, e.message)

    def get_signal_id(self, signal_id):
        signal_id_list = [signal_id]
        return signal_id_list