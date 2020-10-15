from datetime import datetime
import decimal

from numpy.lib.function_base import insert
from sqlalchemy import MetaData, Table, select, or_
from coralquant.database import engine
from coralquant.models.bdl_model import daily_k_data, weekly_k_data, monthly_k_data
from coralquant.models.odl_model import stock_basic
from coralquant.settings import CQ_Config
from coralquant import logger
from coralquant.stringhelper import frequency_tablename

_logger = logger.Logger(__name__).get_log()


def get_bs_stock_code():
    """
    获取bs股票代码
    """
    metadata = MetaData()
    tmp = Table('odl_bs_stock_basic', metadata, autoload=True, autoload_with=engine)
    rp = engine.execute(select([tmp.c.code]).where(or_(tmp.c.type == '1', tmp.c.type == '2')))
    result = []
    for row in rp:
        code = row[0]
        result.append(code)
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


def import_data(frequency: str):
    """
    导入日线数据
    """

    ts_code_list = get_bs_stock_code()
    total = 0  #计算总行数

    if frequency == 'w':

        table_k_data = weekly_k_data
    elif frequency == 'm':
        table_k_data = monthly_k_data
    else:
        table_k_data = daily_k_data

    tablename = frequency_tablename[frequency]
    metadata = MetaData()
    tmp = Table(tablename, metadata, autoload=True, autoload_with=engine)

    with engine.connect() as connection:
        for ts_code in ts_code_list:
            result = engine.execute(select([tmp]).where(tmp.c.code == ts_code))
            daily_k_data_list = []
            step = 0
            ins = table_k_data.insert()
            for row in result:

                tmprow = {
                    'date': datetime.strptime(row.date, "%Y-%m-%d").date(),
                    'code': row.code,
                    'open': get_decimal_from_str(row.open),
                    'high': get_decimal_from_str(row.high),
                    'low': get_decimal_from_str(row.low),
                    'close': get_decimal_from_str(row.close),
                    'volume': get_int_from_str(row.volume),
                    'amount': get_decimal_from_str(row.amount),
                    'adjustflag': row.adjustflag,
                    'turn': get_float_from_str(row.turn),
                    'pctChg': get_float_from_str(row.pctChg),
                }

                if frequency == 'd':
                    tmprow['preclose'] = get_decimal_from_str(row.preclose)
                    tmprow['tradestatus'] = bool(get_int_from_str(row.tradestatus))
                    tmprow['peTTM'] = get_float_from_str(row.peTTM)
                    tmprow['pbMRQ'] = get_float_from_str(row.pbMRQ)
                    tmprow['psTTM'] = get_float_from_str(row.psTTM)
                    tmprow['pcfNcfTTM'] = get_float_from_str(row.pcfNcfTTM)
                    tmprow['isST'] = bool(get_int_from_str(row.isST))

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