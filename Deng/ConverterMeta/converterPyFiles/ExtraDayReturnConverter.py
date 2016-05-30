import json,re
from MiniMOManager.common.Util import is_bool,OrderedObject
from MiniMOManager.common.SignalManager import SignalObject, SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class ExtraDayReturnMeta(OrderedObject):
    def __init__(self):
        super(ExtraDayReturnMeta,self).__init__()
        self.Name=""
        self.Type="ExtraDayReturn"
        self.InstrumentName=""
        self.Enabled=1
        self.NeedSigalDataFromAthene=""
        self.Mode="Autonomy"

    def get_const_member_list(self):
        member_list = ['Name','Type','InstrumentName','Enabled',
            'NeedSigalDataFromAthene','Mode']
        return member_list

    def get_signal_list(self):
        signal_list=[]
        return signal_list

    def get_bool_list(self):
        bool_list=['Enabled', 'NeedSigalDataFromAthene']
        return bool_list

class ExtraDayReturnConverter(object):

    def __init__(self):
        self.__ExtraDayReturn_meta_list = []
        self.__signal_object_list = []

    def set_meat_list(self, ExtraDayReturn_meta_list):
        self.__ExtraDayReturn_meta_list = ExtraDayReturn_meta_list

    def start_converter(self):
        for meta in self.__ExtraDayReturn_meta_list:
            self.strategy_to_json(meta)
        return self.__signal_object_list

    def strategy_to_json(self, ExtraDayReturnMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            is_error = False
            for member in ExtraDayReturnMeta.get_const_member_list():
                member_value = getattr(ExtraDayReturnMeta, member)
                if member in ExtraDayReturnMeta.get_bool_list():
                    data_json[member] = is_bool(getattr(ExtraDayReturnMeta, member))
                elif member in ExtraDayReturnMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        is_error=True
                else:
                    data_json[member] = getattr(ExtraDayReturnMeta, member)
            if not is_error:
                signal_object = SignalObject()
                signal_object.name = ExtraDayReturnMeta.Name
                signal_object.type = ExtraDayReturnMeta.Type
                signal_object.enable = True
                signal_object.node = json.dumps(data_json)
                self.__signal_object_list.append(signal_object)
        except Exception as e:
            raise CSVConverterError(ExtraDayReturnMeta.Name, ExtraDayReturnMeta.Type, e.message)

    def get_signal_id(self, signal_id):
        signal_id_list = [signal_id]
        return signal_id_list