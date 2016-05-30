import json,re
from MiniMOManager.common.Util import is_bool,OrderedObject
from MiniMOManager.common.SignalManager import SignalObject, SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class TradingUniverseMeta(OrderedObject):
    def __init__(self):
        super(TradingUniverseMeta,self).__init__()
        self.Name=""
        self.Type="TradingUniverse"
        self.BalanceDateSignal=""
        self.TradingUniverse=""
        self.Enabled=1
        self.NeedSigalDataFromAthene=""
        self.Mode="Autonomy"

    def get_const_member_list(self):
        member_list = ['Name','Type','BalanceDateSignal','TradingUniverse',
            'Enabled','NeedSigalDataFromAthene','Mode']
        return member_list

    def get_signal_list(self):
        signal_list=['BalanceDateSignal']
        return signal_list

    def get_function_dict(self):
        function_dict={'TradingUniverse': ['GetTradingUniverse', [0]]}
        return function_dict

    def get_bool_list(self):
        bool_list=['Enabled', 'NeedSigalDataFromAthene']
        return bool_list

class TradingUniverseConverter(object):

    def __init__(self):
        self.__TradingUniverse_meta_list = []
        self.__signal_object_list = []

    def set_meat_list(self, TradingUniverse_meta_list):
        self.__TradingUniverse_meta_list = TradingUniverse_meta_list

    def start_converter(self):
        for meta in self.__TradingUniverse_meta_list:
            self.strategy_to_json(meta)
        return self.__signal_object_list

    def strategy_to_json(self, TradingUniverseMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            is_error = False
            for member in TradingUniverseMeta.get_const_member_list():
                member_value = getattr(TradingUniverseMeta, member)
                if member in TradingUniverseMeta.get_bool_list():
                    data_json[member] = is_bool(getattr(TradingUniverseMeta, member))
                elif member in TradingUniverseMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        is_error=True
                else:
                    data_json[member] = getattr(TradingUniverseMeta, member)
            for key,value in TradingUniverseMeta.get_function_dict():
                param = re.split(r'[\(\)]+',data_json[key].strip())
                param = re.split(r',',param[1].strip())
                for i,e in enumerate(value[1]):
                    if e == 1:
                        param[i] = "TradingUniverseMeta."+param[i]
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
                signal_object.name = TradingUniverseMeta.Name
                signal_object.type = TradingUniverseMeta.Type
                signal_object.enable = True
                signal_object.node = json.dumps(data_json)
                self.__signal_object_list.append(signal_object)
        except Exception as e:
            raise CSVConverterError(TradingUniverseMeta.Name, TradingUniverseMeta.Type, e.message)

    def get_signal_id(self, signal_id):
        signal_id_list = [signal_id]
        return signal_id_list