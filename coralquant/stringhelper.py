# -*- coding: utf-8 -*-
from coralquant.models.bdl_model import DailyKData, DailyKData2, MonthlyKData, MonthlyKData2, WeeklyKData, WeeklyKData2
from coralquant.models.odl_model import D2_History_A_Stock_K_Data, D_History_A_Stock_K_Data, M2_History_A_Stock_K_Data, M_History_A_Stock_K_Data, T52_History_A_Stock_K_Data, T5_History_A_Stock_K_Data, W2_History_A_Stock_K_Data, W_History_A_Stock_K_Data
from enum import Enum,unique

@unique
class TaskEnum(Enum):
    """
    任务枚举
    """
    日线历史A股K线数据 = 'd'
    周线历史A股K线数据 = 'w'
    月线历史A股K线数据 = 'm'
    T5分钟线历史A股K线数据 = '5'
    季频盈利能力 = 'profit'



frequency_odl_table_obj = {
    'd': D_History_A_Stock_K_Data,
    'w': W_History_A_Stock_K_Data,
    'm': M_History_A_Stock_K_Data,
    '5': T5_History_A_Stock_K_Data,
    'd-2': D2_History_A_Stock_K_Data,
    'w-2': W2_History_A_Stock_K_Data,
    'm-2': M2_History_A_Stock_K_Data,
    '5-2': T52_History_A_Stock_K_Data

}

frequency_bdl_table_obj = {
    'd': DailyKData,
    'w': WeeklyKData,
    'm': MonthlyKData,
    'd-2': DailyKData2,
    'w-2': WeeklyKData2,
    'm-2': MonthlyKData2
    #'5': T5_History_A_Stock_K_Data
}
