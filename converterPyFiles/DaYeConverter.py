import json
from MiniMOManager.common.Util import is_bool,OrderedObject
from MiniMOManager.common.SignalManager import SignalObject, SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class DaYeMeta(OrderedObject):
    def __init__(self):
        super(DaYeMeta,self).__init__()
        self.Name=""
        self.Type="DaYe"
        self.CloseDay=""
        self.DependentSignalId=""
        self.Interval=""
        self.ClosePosTime=""
        self.OpenPosTime=""
        self.NeedSigalDataFromAthene=""
        self.Mode="Autonomy"

    def get_const_member_list(self):
        member_list = ['Name','Type','CloseDay','DependentSignalId',
            'Interval','ClosePosTime','OpenPosTime',
            'NeedSigalDataFromAthene','Mode']
        return member_list

    def get_signal_list(self):
        signal_list=[]
        return signal_list

    def get_bool_list(self):
        bool_list=['NeedSigalDataFromAthene']
        return bool_list

class DaYeConverter(object):

    def __init__(self):
        self.__DaYe_meta_list = []
        self.__signal_object_list = []

    def set_meat_list(self, DaYe_meta_list):
        self.__DaYe_meta_list = DaYe_meta_list

    def start_converter(self):
        for meta in self.__DaYe_meta_list:
            self.strategy_to_json(meta)
        return self.__signal_object_list

    def strategy_to_json(self, DaYeMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            is_error = False
            for member in DaYeMeta.get_const_member_list():
                member_value = getattr(DaYeMeta, member)
                if member in DaYeMeta.get_bool_list():
                    data_json[member] = is_bool(getattr(DaYeMeta, member))
                elif member in DaYeMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        raise CSVConverterError(DaYeMeta.Name, DaYeMeta.Type, "Can't find signal: {0}".format(member_value))
                else:
                    data_json[member] = getattr(DaYeMeta, member)
            if not is_error:
                signal_object = SignalObject()
                signal_object.name = DaYeMeta.Name
                signal_object.type = DaYeMeta.Type
                signal_object.enable = True
                signal_object.node = json.dumps(data_json)
                self.__signal_object_list.append(signal_object)
        except Exception as e:
            raise CSVConverterError(DaYeMeta.Name, DaYeMeta.Type, e.message)

    def get_signal_id(self, signal_id):
        signal_id_list = [signal_id]
        return signal_id_list