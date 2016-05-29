__author__ = 'jiayun.wei'
#strategy
if member in ['MatchStrategyId']:
data_json[member] = (get_strategy_id_by_name(self.work_dir, member_value), member_value)[isinstance(member_value, int)]

#portfolio
if member in ["Portfolio",'llll']:
data_json[member] = reference_portfolio(member_value)
if data_json[member] == -1:
raise CSVConverterError(JiXian_meta.Name, JiXian_meta.Type, "Can't find portfolio: {0}".format(member_value))


#signal
if member in JiXian_meta.get_signal_list():
data_json[member] = (signal_finder.get_signal_id_by_name(member_value), member_value)[isinstance(member_value, int)]
if data_json[member] == -1:
raise CSVConverterError(JiXian_meta.Name, JiXian_meta.Type, "Can't find signal: {0}".format(member_value))


#bool
if member in ['IsImmediately', "Enabled"]:
data_json[member] = is_bool(member_value)

#get_args
member_value = LaoZi_meta.LaoZi
param = '{0}( {1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13} )'.format(member_value
,LaoZi_meta.InstrumentName
,LaoZi_meta.DateTime
,LaoZi_meta.length
,LaoZi_meta.STDType
,LaoZi_meta.DayOpenTimeRanges_START6
,LaoZi_meta.DayOpenTimeRanges_END6
,LaoZi_meta.NightOpenTimeRanges_START5
,LaoZi_meta.NightOpenTimeRanges_END5
,LaoZi_meta.DayCloseTimeRanges_START4
,LaoZi_meta.DayCloseTimeRanges_END4
,LaoZi_meta.NightCloseTimeRanges_START3
,LaoZi_meta.NightCloseTimeRanges_END3
,LaoZi_meta.CrossDay)
data_json['LaoZi'] = reference_arg_manager(param)

#instruments
data_json['Instruments'] = generate_instruments(ShuangQiao_meta, ShuangQiao_meta.member_list)

#ranges
data_json['Ranges'] = generate_ranges(ShuangQiao_meta, ShuangQiao_meta.member_list)