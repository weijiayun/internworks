__author__ = '__main__'

import json
from MiniMOManager.common.BPManager import BPManager
from MiniMOManager.common.SignalManager import SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class AutomatonMeta(OrderedObject):
    def __init__(self):
        super(AutomatonMeta,self).__init__()
        self.Name = ""
        self.Type = "Automaton"
        self.SplitTyoExchange = ""
        self.MaxOrderQty = ""
        self.CloseYdPriorityQue = ""
        self.SplitType = "ShyGirl"
        self.Strategies = ""
        self.Components = ""

    def get_const_member_list(self):
        member_list = ['Name','Type','SplitTyoExchange','MaxOrderQty',
            'CloseYdPriorityQue','SplitType','Strategies',
            'Components']
        return member_list

    def get_signal_list(self):
        signal_list = []
        return signal_list

    def required_member_list(self):
        required_list=['Name', 'Type', 'SplitTyoExchange', 'MaxOrderQty', 'CloseYdPriorityQue', 'SplitType', 'Strategies', 'Components']
        return required_list

    def optional_member_list(self):
        optional_list=[]
        return optional_list

    def get_bool_list(self):
        bool_list = []
        return bool_list

    def get_strategy_csv_header(self):
        header_list = []
        for header in dir(self):
            if header[:2] != '__' and header[-2:] != '__' and header[:4] != 'get_':
                header_list.append(header)
        return header_list

    def get_portfolio_list(self):
        portfolio_list = ['Portfolio']
        return portfolio_list

    def get_MatchStrategyId(self):
        ID_list = ['MatchStrategyId']
        return ID_list

class AutomatonConverter(object):
    def __init__(self, work_dir=None):
        self.id = float('nan')
        self.__Automaton_meta_list = []
        self.work_dir = work_dir
        self.__bp_manager = None
        
    def set_meat_list(self, HeFeiV3_meta_list):
        self.__Automaton_meta_list = HeFeiV3_meta_list

    def get_meat_list(self):
        return self.__Automaton_meta_list

    def init_bp_manager(self):
        if self.__bp_manager is None:
            self.__bp_manager = BPManager()

    def init_strategy_id(self):
        self.id = get_max_id(self.work_dir)
        if self.id == -1:
            self.id = self.__bp_manager.get_max_portfolio_id()

    def start_converter(self):
        self.init_bp_manager()
        self.init_strategy_id()
        for meta in self.__Automaton_meta_list:
            self.strategy_to_json(meta)

    def strategy_to_json(self, AutomatonMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            for member in AutomatonMeta.get_const_member_list():
                member_value = getattr(AutomatonMeta, member)
                if member in AutomatonMeta.get_portfolio_list():
                    data_json[member] = reference_portfolio(member_value)
                    if data_json[member] == -1:
                        raise CSVConverterError(AutomatonMeta.Name, AutomatonMeta.Type, "Can't find portfolio: {0}".format(member_value))
                elif member in AutomatonMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        raise CSVConverterError(AutomatonMeta.Name, AutomatonMeta.Type, "Can't find signal: {0}".format(member_value))

                elif member in AutomatonMeta.get_bool_list():
                    data_json[member] = is_bool(member_value)
                elif member in AutomatonMeta.get_MatchStrategyId():
                    data_json[member] = (get_strategy_id_by_name(self.work_dir, member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        raise CSVConverterError(AutomatonMeta.Name, AutomatonMeta.Type, "Can't find matchstrategy:{0}".format(member_value))
                else:
                    data_json[member] = member_value
            data_json['Instruments'] = generate_instruments(AutomatonMeta, AutomatonMeta.member_list)
            data_json['Ranges'] = generate_ranges(AutomatonMeta, AutomatonMeta.member_list)
        except Exception as e:
            raise CSVConverterError(AutomatonMeta.Name, AutomatonMeta.Type, e.message)
        if self.work_dir is not None:
            self.__create_file(data_json)
        return data_json
    def __create_file(self, data):
        self.id += 1
        data['Id'] = self.id
        file_path = '{0}/Existed_Json_Module/{1:0>4}{2}.strategy'.format(self.work_dir, data['Id'], data['Name'])
        json.dump([data], open(file_path, 'w'))
        return self.id

