from coralquant.taskmanage import create_bs_task
from coralquant.util.dataconvert import get_decimal_from_str, get_int_from_str
from coralquant import logger
from datetime import datetime
from coralquant.models.odl_model import BS_Daily_hfq
from coralquant.stringhelper import TaskEnum
from coralquant.odl.baostock.util import query_history_k_data_plus
from coralquant.database import engine

_logger = logger.Logger(__name__).get_log()

def update_task(reset: bool = False):
    """
    更新任务表
    """
    create_bs_task(TaskEnum.BS日线历史A股K线后复权数据)


def _load_data(dic:dict):
    """
    docstring
    """
    content=dic['result']
    bs_code=dic['bs_code']
    frequency=dic['frequency']
    adjustflag=dic['adjustflag']

    if content.empty:
        return

    table_name = BS_Daily_hfq.__tablename__

    try:

        content['date'] = [datetime.strptime(x, '%Y-%m-%d').date() for x in content['date']]
        #content['code'] = 
        content['open'] = [None if x == "" else get_decimal_from_str(x) for x in content["open"]]
        content['high'] = [None if x == "" else get_decimal_from_str(x) for x in content["high"]]
        content['low'] = [None if x == "" else get_decimal_from_str(x) for x in content["low"]]
        content['close'] = [None if x == "" else get_decimal_from_str(x) for x in content["close"]]
        content['preclose'] = [None if x == "" else get_decimal_from_str(x) for x in content["preclose"]]
        content['volume'] = [None if x == "" else get_int_from_str(x) for x in content["volume"]]
        content['amount'] = [None if x == "" else get_decimal_from_str(x) for x in content["amount"]]
        #content['adjustflag'] = 
        content['turn'] = [None if x == "" else get_decimal_from_str(x) for x in content["turn"]]
        content['tradestatus'] = [None if x == "" else bool(get_int_from_str(x)) for x in content["tradestatus"]] 
        content['pctChg'] = [None if x == "" else get_decimal_from_str(x) for x in content["pctChg"]]
        content['peTTM'] = [None if x == "" else get_decimal_from_str(x) for x in content["peTTM"]]
        content['psTTM'] = [None if x == "" else get_decimal_from_str(x) for x in content["psTTM"]]
        content['pcfNcfTTM'] = [None if x == "" else get_decimal_from_str(x) for x in content["pcfNcfTTM"]]
        content['pbMRQ'] = [None if x == "" else get_decimal_from_str(x) for x in content["pbMRQ"]]
        content['isST'] = [None if x == "" else bool(get_int_from_str(x)) for x in content["isST"]]

        content.to_sql(table_name, engine, schema='stock_dw', if_exists='append', index=False)

    except Exception as e:  #traceback.format_exc(1)
        _logger.error('{}保存出错/{}'.format(bs_code, repr(e)))


def get_daily_hfq():
    """
    按照任务表，获取BS日线后复权行情数据
    """

    query_history_k_data_plus(TaskEnum.BS日线历史A股K线后复权数据,'d','1',_load_data,{})