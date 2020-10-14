from datetime import datetime
import random
import time

import baostock as bs
import pandas as pd
from sqlalchemy import select

from coralquant import logger
from coralquant.models.odl_model import stock_basic
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import session_maker, TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.database import engine

_logger = logger.Logger(__name__).get_log()


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


def query_history_k_data_plus(ts_code: str, fields: str, start_date: str, end_date: str, frequency: str,
                              adjustflag: str) -> pd.DataFrame:
    """
    获取历史A股K线数据
    """
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    _logger.info('login respond error_code:' + lg.error_code)
    _logger.info('login respond  error_msg:' + lg.error_msg)

    rs = bs.query_history_k_data_plus(ts_code,
                                      fields,
                                      start_date=start_date,
                                      end_date=end_date,
                                      frequency=frequency,
                                      adjustflag=adjustflag)
    _logger.info('query_history_k_data_plus respond error_code:' + rs.error_code)
    _logger.info('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 登出系统 ####
    bs.logout()
    return result


def init_history_k_data_plus(frequency,
                             adjustflag="3"):
    """
    初始化历史K线数据
    """
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

    frequency_tablename = {
        'd': 'odl_d_history_A_stock_k_data',
        'w': 'odl_w_history_A_stock_k_data',
        'm': 'odl_m_history_A_stock_k_data',
        '5': 'odl_5_history_A_stock_k_data',
        '15': 'odl_15_history_A_stock_k_data',
        '30': 'odl_30_history_A_stock_k_data',
        '60': 'odl_60_history_A_stock_k_data'
    }
    table_name = frequency_tablename[frequency]

    with session_maker() as sm:
        rp = sm.query(TaskTable).filter(TaskTable.task == TaskEnum.获取历史A股K线数据.value, TaskTable.finished == False).limit(3)
        step = 1
        for task in rp:
            try:
                if task.finished:
                    continue

                sleep = random.random() * 1
                time.sleep(sleep)

                start_date = task.begin_date.strftime("%Y-%m-%d")
                end_date = task.end_date.strftime("%Y-%m-%d")
                result = query_history_k_data_plus(task.ts_code, fields, start_date, end_date, frequency, adjustflag)

                result.to_sql(table_name,
                              engine,
                              schema='stock_dw',
                              if_exists='replace' if step == 1 else 'append',
                              index=False)
                step += 1
            except Exception as e:
                _logger.error("{}下载失败,no.{}".format(task.ts_code, step))
            else:
                task.finished=True
                _logger.info("完成{}下载,no.{}".format(task.ts_code, step))
        
        sm.commit()
