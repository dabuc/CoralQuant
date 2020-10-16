from datetime import datetime
import random
import time
import decimal

import baostock as bs
import pandas as pd
from sqlalchemy import select
from coralquant.database import engine
from sqlalchemy import Integer, Numeric, String, Enum, Float, Boolean, BigInteger, Date

from coralquant import logger
from coralquant.models.odl_model import stock_basic
from coralquant.settings import CQ_Config


def get_task_list():
    """
    获取股票列表
    """
    s = select([stock_basic.c.ts_code]).where(stock_basic.c.list_status == 'L')
    rp = engine.execute(s)
    task_list = []
    for row in rp:
        a = row[0].split('.')
        code = '{}.{}'.format(a[1].lower(), a[0])
        iscmpl = False
        task = [code, iscmpl]
        task_list.append(task)
    return task_list


def init_history_k_data_plus(frequency,
                             table_name,
                             start_date='1990-12-19',
                             end_date=datetime.now().strftime("%Y-%m-%d"),
                             adjustflag="3"):
    """
    初始化历史K线数据
    """
    _logger = logger.Logger(__name__).get_log()

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    _logger.info("login respond error_code:" + lg.error_code)
    _logger.info("login respond  error_msg:" + lg.error_msg)

    d_fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
    w_m_fields = 'date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg'
    min_fields = 'date,time,code,open,high,low,close,volume,amount,adjustflag'

    frequency_fields = {
        'd': d_fields,
        'w': w_m_fields,
        'm': w_m_fields,
        '5': min_fields,
        '15': min_fields,
        '30': min_fields,
        '60': min_fields
    }

    fields = frequency_fields[frequency]

    task_list = get_task_list()
    step = 1
    for task in task_list:
        try:
            if task[1]:
                continue

            sleep = random.random() * 1
            time.sleep(sleep)

            #### 获取历史K线数据 ####
            # 详细指标参数，参见“历史行情指标参数”章节
            rs = bs.query_history_k_data_plus(
                task[0],
                fields,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                adjustflag=adjustflag,
            )  # frequency="d"取日k线，adjustflag="3"默认不复权
            _logger.info("query_history_k_data_plus respond error_code:" + rs.error_code)
            _logger.info("query_history_k_data_plus respond  error_msg:" + rs.error_msg)

            #### 打印结果集 ####
            data_list = []
            while (rs.error_code == "0") & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)

            #w_m_fields='date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg'
            #d_fields="preclose,tradestatus,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",

            
            result["date"] = [datetime.strptime(x, "%Y-%m-%d").date() for x in result["date"]]
            result["open"] = [0 if x == "" else decimal.Decimal(x) for x in result["open"]]
            result["high"] = [0 if x == "" else decimal.Decimal(x) for x in result["high"]]
            result["low"] = [0 if x == "" else decimal.Decimal(x) for x in result["low"]]
            result["close"] = [0 if x == "" else decimal.Decimal(x) for x in result["close"]]
            result["volume"] = [0 if x == "" else int(x) for x in result["volume"]]
            result["amount"] = [0 if x == "" else decimal.Decimal(x) for x in result["amount"]]

            if frequency in ['d', 'w', 'm']:
                result["turn"] = [0 if x == "" else float(x) for x in result["turn"]]
                result["pctChg"] = [0 if x == "" else float(x) for x in result["pctChg"]]

            if frequency == 'd':
                result["preclose"] = [0 if x == "" else decimal.Decimal(x) for x in result["preclose"]]
                result["peTTM"] = [0 if x == "" else float(x) for x in result["peTTM"]]
                result["pbMRQ"] = [0 if x == "" else float(x) for x in result["pbMRQ"]]
                result["psTTM"] = [0 if x == "" else float(x) for x in result["psTTM"]]
                result["pcfNcfTTM"] = [0 if x == "" else float(x) for x in result["pcfNcfTTM"]]

            dtype = {
                'date': Date,
                'code': String(10),
                'open': Numeric(12, 4),
                'high': Numeric(12, 4),
                'low': Numeric(12, 4),
                'close': Numeric(12, 4),
                'preclose': Numeric(12, 4),
                'volume': BigInteger(),
                'amount': Numeric(23, 4),
                'adjustflag': Enum('1', '2', '3'),
                'turn': Float(),
                'tradestatus': Boolean(),
                'pctChg': Float(),
                'peTTM': Float(),
                'pbMRQ': Float(),
                'psTTM': Float(),
                'pcfNcfTTM': Float(),
                'isST': Boolean()
            }

            result.to_sql(table_name,
                        engine,
                        schema='stock_dw',
                        if_exists='replace' if step == 1 else 'append',
                        index=False,
                        dtype=dtype)
            step += 1
        except Exception as e:
            _logger.error("{}下载失败,no.{}".format(task[0], step))
        else:
            task[1] = True
            _logger.info("完成{}下载,no.{}".format(task[0], step))

    #### 登出系统 ####
    bs.logout()



if __name__ == "__main__":
    pass