import concurrent.futures
from coralquant.util.dataconvert import get_decimal_from_str, get_float_from_str, get_int_from_str
import decimal
from datetime import datetime

from coralquant import logger
from coralquant.database import  session_scope
from coralquant.stringhelper import (frequency_bdl_table_obj, frequency_odl_table_obj)
from sqlalchemy.sql import func

_logger = logger.Logger(__name__).get_log()


def _build_result_data(rp, frequency):
    """
    构建结果数据列表
    """
    result = []
    for row in rp:
        tmp = {
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
            tmp['preclose'] = get_decimal_from_str(row.preclose)
            tmp['tradestatus'] = bool(get_int_from_str(row.tradestatus))
            tmp['peTTM'] = get_float_from_str(row.peTTM)
            tmp['pbMRQ'] = get_float_from_str(row.pbMRQ)
            tmp['psTTM'] = get_float_from_str(row.psTTM)
            tmp['pcfNcfTTM'] = get_float_from_str(row.pcfNcfTTM)
            tmp['isST'] = bool(get_int_from_str(row.isST))
        result.append(tmp)
    return result


def _insert_data(data: list, frequency,table_name_key, pagenum):
    """
    导入数据
    """
    ins_data = []
    num = 0  #计数
    try:
        with session_scope() as session:
            for dic in data:
                to_table = frequency_bdl_table_obj[table_name_key]()
                to_table.date = dic['date']
                to_table.code = dic['code']
                to_table.open = dic['open']
                to_table.high = dic['high']
                to_table.low = dic['low']
                to_table.close = dic['close']
                to_table.volume = dic['volume']
                to_table.amount = dic['amount']
                to_table.adjustflag = dic['adjustflag']
                to_table.turn = dic['turn']
                to_table.pctChg = dic['pctChg']
                if frequency == 'd':
                    to_table.preclose = dic['preclose']
                    to_table.tradestatus = dic['tradestatus']
                    to_table.peTTM = dic['peTTM']
                    to_table.pbMRQ = dic['pbMRQ']
                    to_table.psTTM = dic['psTTM']
                    to_table.pcfNcfTTM = dic['pcfNcfTTM']
                    to_table.isST = dic['isST']

                    to_table.float_share = 0 if dic['turn'] ==0 else dic['volume']/dic['turn']/100 

                ins_data.append(to_table)
                num += 1
                dm = divmod(num, 1000)
                if dm[1] == 0:
                    session.bulk_save_objects(ins_data)
                    session.commit()
                    ins_data.clear()
            if len(ins_data) > 0:
                session.bulk_save_objects(ins_data)
                session.commit()
    except Exception as e:
        _logger.error("第{}页数据导入失败:{}".format(pagenum, repr(e)))
    else:
        _logger.info("第{}页数据导入完成".format(pagenum))


def import_data(frequency: str, adjustflag="3"):
    """
    导入日线数据
    """
    #offset：当偏移量大于800万时，offset limit模式性能下降严重，查询一次要12秒……
    #改成直接定位主键id查询。

    if adjustflag !='3':
        table_name_key = '{}-{}'.format(frequency,adjustflag)
    else:
        table_name_key = frequency

    from_table = frequency_odl_table_obj[table_name_key]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as session:
            onerow = session.query(func.min(from_table.id), func.max(from_table.id)).one()
            minid = onerow[0]
            maxid = onerow[1]

            if not minid:  #没有数据
                return

            pagesize = 5000
            ahead_id = minid
            next_id = ahead_id + pagesize
            i = 0  #计数
            while True:
                if ahead_id > maxid:
                    break
                rp = session.query(from_table).filter(from_table.id >= ahead_id, from_table.id < next_id)
                to_data = _build_result_data(rp, frequency)
                executor.submit(_insert_data, to_data, frequency,table_name_key, i + 1)
                i += 1
                ahead_id = next_id
                next_id = ahead_id + pagesize

    _logger.info("数据导入完成")


if __name__ == "__main__":
    pass
