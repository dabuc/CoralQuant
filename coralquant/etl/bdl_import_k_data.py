import math
from coralquant.database import session_maker,get_new_session
from coralquant.models.odl_model import D_History_A_Stock_K_Data, M_History_A_Stock_K_Data, T5_History_A_Stock_K_Data
from datetime import datetime
import decimal

from coralquant.models.bdl_model import DailyKData , WeeklyKData, MonthlyKData
from coralquant import logger
import concurrent.futures

_logger = logger.Logger(__name__).get_log()


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


frequency_from_table = {
    'd': D_History_A_Stock_K_Data,
    'w': M_History_A_Stock_K_Data,
    'm': M_History_A_Stock_K_Data,
    '5': T5_History_A_Stock_K_Data
}

frequency_to_table = {
    'd': DailyKData,
    'w': WeeklyKData,
    'm': MonthlyKData
    #'5': T5_History_A_Stock_K_Data
}

def _build_result_data(rp,frequency):
    """
    构建结果数据列表
    """
    result=[]
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

def _insert_data(data:list,frequency,pagenum):
    """
    导入数据
    """
    session = get_new_session()
    ins_data=[]
    num = 0 #计数
    try:
        with session_maker(session) as session:
            for dic in data:   
                to_table= frequency_to_table[frequency]()
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
                    to_table.preclose=dic['preclose'] 
                    to_table.tradestatus=dic['tradestatus']
                    to_table.peTTM=dic['peTTM']
                    to_table.pbMRQ=dic['pbMRQ']
                    to_table.psTTM=dic['psTTM']
                    to_table.pcfNcfTTM=dic['pcfNcfTTM']
                    to_table.isST=dic['isST']
                ins_data.append(to_table)
                num+=1
                dm = divmod(num, 1000)
                if dm[1] == 0:
                    session.bulk_save_objects(ins_data)
                    session.commit()
                    ins_data.clear()
            if len(ins_data) > 0:
                session.bulk_save_objects(ins_data)
                session.commit()
    except Exception as e:
        _logger.error("第{}页数据导入失败:{}".format(pagenum,repr(e)))
    else:
        _logger.info("第{}页数据导入完成".format(pagenum))


def import_data(frequency: str):
    """
    导入日线数据
    """

    from_table = frequency_from_table[frequency]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_maker() as session:
            rowsnum= session.query(from_table).count()
            pagesize=5000
            pagenum = math.ceil(rowsnum/ pagesize)
            thread_list=[]
            for i in range(0,pagenum):
                rp=session.query(from_table).offset(pagesize*i).limit(pagesize)
                to_data= _build_result_data(rp,frequency)
                executor.submit(_insert_data, to_data, frequency,i+1)

if __name__ == "__main__":
    pass