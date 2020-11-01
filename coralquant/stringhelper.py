# -*- coding: utf-8 -*-
from coralquant.models.bdl_model import DailyKData, MonthlyKData, WeeklyKData
from coralquant.models.odl_model import D_History_A_Stock_K_Data, M_History_A_Stock_K_Data, T5_History_A_Stock_K_Data, W_History_A_Stock_K_Data
from enum import Enum,unique

@unique
class TaskEnum(Enum):
    """
    任务枚举
    """
    日线历史A股K线数据 = 'd'
    周线历史A股K线数据 = 'w'
    月线历史A股K线数据 = 'm'
    季频盈利能力 = 'profit'



frequency_odl_table_obj = {
    'd': D_History_A_Stock_K_Data,
    'w': W_History_A_Stock_K_Data,
    'm': M_History_A_Stock_K_Data,
    '5': T5_History_A_Stock_K_Data
}

frequency_bdl_table_obj = {
    'd': DailyKData,
    'w': WeeklyKData,
    'm': MonthlyKData
    #'5': T5_History_A_Stock_K_Data
}
