__author__ = '__main__'

import json
from MiniMOManager.common.BPManager import BPManager
from MiniMOManager.common.SignalManager import SignalFinder
from MiniMOManager.common.Util import get_max_id, is_bool, is_instrument_name, OrderedObject, CSVConverterError, get_strategy_id_by_name
from MiniMOManager.common.ConverterManager.Util import reference_portfolio, generate_ranges, generate_instruments, reference_HeFeiSub, reference_arg_manager

class HFStrategyMeta(OrderedObject):
    def __init__(self):
        super(HFStrategyMeta,self).__init__()
        self.Name=""
        self.Type="HFStrategy"
        self.MinMaxPositionChangePercent=""
        self.XN=""
        self.XD=""
        self.IsNightTrade=True
        self.IsDayTrade=True
        self.OrderType="OTGFD"
        self.MatchType=""
        self.Market=""
        self.Action1=""
        self.START1=""
        self.END1=""
        self.EmitterType=""
        self.PreHardCloseSpread=0
        self.GTNBWaitTime=1000
        self.GTNBTolerance=0
        self.HCslip=5
        self.Instruments_InstrumentName1=""
        self.Instruments_IsConnect1=""
        self.Instruments_Market1=""
        self.Portfolio=""
        self.Enabled=1

    def get_const_member_list(self):
        member_list = ['Name','Type','MinMaxPositionChangePercent','XN',
            'XD','IsNightTrade','IsDayTrade',
            'OrderType','MatchType','Market',
            'EmitterType','PreHardCloseSpread','GTNBWaitTime',
            'GTNBTolerance','HCslip','Portfolio',
            'Enabled']
        return member_list

    def get_signal_list(self):
        signal_list = ['signal']
        return signal_list

    def get_strategy_csv_header(self):
        header_list = []
        for header in dir(self):
            if header[:2] != '__' and header[-2:] != '__' and header[:4] != 'get_':
                header_list.append(header)
        return header_list

    def get_portfolio_list(self):
        portfolio_list = ['Portfolio']
        return portfolio_list

    def get_bool_list(self):
        bool_list=['IsNightTrade', 'IsDayTrade', 'Enabled']
        return bool_list

    def get_MatchStrategyId(self):
        ID_list=['MatchStrategyId']
        return ID_list

class HFStrategyConverter(object):
    def __init__(self, work_dir=None):
        self.id = float('nan')
        self.__HFStrategy_meta_list = []
        self.work_dir = work_dir
        self.__bp_manager = None
        
    def set_meat_list(self, HeFeiV3_meta_list):
        self.__HFStrategy_meta_list = HeFeiV3_meta_list

    def get_meat_list(self):
        return self.__HFStrategy_meta_list

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
        for meta in self.__HFStrategy_meta_list:
            self.strategy_to_json(meta)

    def strategy_to_json(self, HFStrategyMeta):
        data_json = {}
        try:
            signal_finder = SignalFinder()
            for member in HFStrategyMeta.get_const_member_list():
                member_value = getattr(HFStrategyMeta, member)
                if member in HFStrategyMeta.get_portfolio_list():
                    data_json[member] = reference_portfolio(member_value)
                    if data_json[member] == -1:
                        raise CSVConverterError(HFStrategyMeta.Name, HFStrategyMeta.Type, "Can't find portfolio: {0}".format(member_value))
                elif member in HFStrategyMeta.get_signal_list():
                    data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        raise CSVConverterError(HFStrategyMeta.Name, HFStrategyMeta.Type, "Can't find signal: {0}".format(member_value))

                elif member in HFStrategyMeta.get_bool_list():
                    data_json[member] = is_bool(member_value)
                elif member in HFStrategyMeta.get_MatchStrategyId():
                    data_json[member] = (get_strategy_id_by_name(self.work_dir, member_value), member_value)[isinstance(member_value, int)]
                    if data_json[member] == -1:
                        raise CSVConverterError(HFStrategyMeta.Name, HFStrategyMeta.Type, "Can't find matchstrategy:{0}".format(member_value))
                else:
                    data_json[member] = member_value
            data_json['Instruments'] = generate_instruments(HFStrategyMeta, HFStrategyMeta.member_list)
            data_json['Ranges'] = generate_ranges(HFStrategyMeta, HFStrategyMeta.member_list)
        except Exception as e:
            raise CSVConverterError(HFStrategyMeta.Name, HFStrategyMeta.Type, e.message)
        if self.work_dir is not None:
            self.__create_file(data_json)
        return data_json
    def __create_file(self, data):
        self.id += 1
        data['Id'] = self.id
        file_path = '{0}/Existed_Json_Module/{1:0>4}{2}.strategy'.format(self.work_dir, data['Id'], data['Name'])
        json.dump([data], open(file_path, 'w'))
        return self.id

