# -*- coding: utf-8 -*-
from enum import IntEnum,unique

@unique
class TaskEnum(IntEnum):
    """
    docstring
    """
    获取历史A股K线数据 = 1


frequency_tablename = {
    'd': 'odl_d_history_A_stock_k_data',
    'w': 'odl_w_history_A_stock_k_data',
    'm': 'odl_m_history_A_stock_k_data',
    '5': 'odl_5_history_A_stock_k_data',
    '15': 'odl_15_history_A_stock_k_data',
    '30': 'odl_30_history_A_stock_k_data',
    '60': 'odl_60_history_A_stock_k_data'
}
