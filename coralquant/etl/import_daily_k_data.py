from datetime import datetime
import decimal

import pandas as pd
from dotenv.main import get_key
from numpy.lib.function_base import insert
from sqlalchemy import MetaData, Table, create_engine, select

from coralquant.models.odl_model import daily_k_data, stock_basic
from coralquant.settings import CQ_Config
from coralquant import logger

_logger = logger.Logger(__name__).get_log()
engine = create_engine(CQ_Config.DATABASE_URL)


def get_bs_stock_code():
    """
    获取bs股票代码
    """
    s = select([stock_basic.c.ts_code])
    rp = engine.execute(s)
    result = []
    for row in rp:
        s = row.ts_code.split('.')
        new_s = '{}.{}'.format(s[1].lower(), s[0])
        result.append(new_s)
    return result


def get_decimal_from_str(str):
    """
    字符串转Decimal
    """
    r = 0 if str == "" else decimal.Decimal(str)
    return r


def get_int_from_str(str):
    """
    字符串转int
    """
    r = 0 if str == "" else int(str)
    return r


def get_float_from_str(str):
    """
    字符串转float
    """
    r = 0 if str == "" else float(str)
    return r


def import_data():
    """
    导入日线数据
    """
    metadata = MetaData()
    connection = engine.connect()

    ts_code_list = get_bs_stock_code()
    total = 0#计算总行数
    tmp = Table('tmp_history_A_stock_k_data', metadata, autoload=True, autoload_with=engine)

    for ts_code in ts_code_list:
        result = engine.execute(select([tmp]).where(tmp.c.code == ts_code))
        daily_k_data_list = []
        step = 0
        ins = daily_k_data.insert()
        for row in result:

            tmprow = {
                'date': datetime.strptime(row.date, "%Y-%m-%d").date(),
                'code': row.code,
                'open': get_decimal_from_str(row.open),
                'high': get_decimal_from_str(row.high),
                'low': get_decimal_from_str(row.low),
                'close': get_decimal_from_str(row.close),
                'preclose': get_decimal_from_str(row.preclose),
                'volume': get_int_from_str(row.volume),
                'amount': get_decimal_from_str(row.amount),
                'adjustflag': row.adjustflag,
                'turn': get_float_from_str(row.turn),
                'tradestatus': bool(row.tradestatus),
                'pctChg': get_float_from_str(row.pctChg),
                'peTTM': get_float_from_str(row.peTTM),
                'pbMRQ': get_float_from_str(row.pbMRQ),
                'psTTM': get_float_from_str(row.psTTM),
                'pcfNcfTTM': get_float_from_str(row.pcfNcfTTM),
                'isST': bool(row.isST)
            }
            daily_k_data_list.append(tmprow)
            step += 1
            total += 1
            dm = divmod(step, 1000)

            if dm[1] == 0:
                connection.execute(ins, daily_k_data_list)
                daily_k_data_list.clear()
                _logger.info("以完成{}条数据插入".format(dm[0] * 1000))

        if len(daily_k_data_list) > 0:
            connection.execute(ins, daily_k_data_list)
            _logger.info("{}导入{}条数据完成".format(ts_code, step))

    _logger.info("导入{}条数据完成".format(total))


if __name__ == "__main__":
    pass