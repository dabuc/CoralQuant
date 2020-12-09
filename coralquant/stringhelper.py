# -*- coding: utf-8 -*-
from coralquant.models.bdl_model import DailyKData, DailyKData1, DailyKData2, MonthlyKData, MonthlyKData2, WeeklyKData, WeeklyKData2
from coralquant.models.odl_model import D1_History_A_Stock_K_Data, D2_History_A_Stock_K_Data, D_History_A_Stock_K_Data, M_History_A_Stock_K_Data, W_History_A_Stock_K_Data
from enum import Enum, unique


@unique
class TaskEnum(Enum):
    """
    任务枚举
    """
    日线历史A股K线数据 = 'd'
    周线历史A股K线数据 = 'w'
    月线历史A股K线数据 = 'm'
    T5分钟线历史A股K线数据 = '5'

    日线历史A股K线前复权数据 = 'd-2'
    周线历史A股K线前复权数据 = 'w-2'
    月线历史A股K线前复权数据 = 'm-2'

    日线历史A股K线后复权数据 = 'd-1'

    季频盈利能力 = 'profit'

    TS更新每日指标 = 'daily_basic'


frequency_odl_table_obj = {
    'd': D_History_A_Stock_K_Data,
    'w': W_History_A_Stock_K_Data,
    'm': M_History_A_Stock_K_Data,
    'd-2': D2_History_A_Stock_K_Data,
    'd-1': D1_History_A_Stock_K_Data,
}

frequency_bdl_table_obj = {
    'd': DailyKData,
    'w': WeeklyKData,
    'm': MonthlyKData,
    'd-2': DailyKData2,
    'w-2': WeeklyKData2,
    'm-2': MonthlyKData2,
    'd-1': DailyKData1

    #'5': T5_History_A_Stock_K_Data
}
