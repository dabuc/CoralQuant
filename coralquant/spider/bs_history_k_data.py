from datetime import datetime
import random
import time

import baostock as bs
import pandas as pd
from sqlalchemy import select
import traceback

from coralquant import logger
from coralquant.models.odl_model import stock_basic
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.database import engine, session_maker
from threading import Thread
from coralquant.stringhelper import frequency_tablename

_logger = logger.Logger(__name__).get_log()

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


def _parse_data(content, ts_code, frequency, is_first):
    """
    解析数据，并保存
    """
    table_name = frequency_tablename[frequency]

    try:
        content.to_sql(table_name, engine, schema='stock_dw', if_exists='replace' if is_first else 'append', index=True)
    except Exception as e:
        _logger.error('{}保存出错：{}'.format(ts_code, traceback.format_exc(1)))
    else:
        _logger.info('{}保存成功'.format(ts_code))


def _query_history_k_data_plus(fields: str, frequency: str, adjustflag: str) -> pd.DataFrame:
    """
    获取历史A股K线数据
    """

    #### 登陆系统 ####
    lg = bs.login()

    step = 1
    with session_maker() as sm:
        rp = sm.query(TaskTable).filter(TaskTable.task == TaskEnum.获取历史A股K线数据.value,
                                        TaskTable.finished == False).limit(20)
        for task in rp:
            if task.finished:
                continue

            start_date = task.begin_date.strftime("%Y-%m-%d")
            end_date = task.end_date.strftime("%Y-%m-%d")

            max_try = 8  # 失败重连的最大次数

            for i in range(max_try):
                rs = bs.query_history_k_data_plus(task.ts_code,
                                                  fields,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  frequency=frequency,
                                                  adjustflag=adjustflag)
                if rs.error_code == '0':
                    _logger.info('{}下载成功'.format(task.ts_code))
                    # executor = ThreadPoolExecutor()
                    # executor.submit(_parse_data)
                    data_list = []
                    while (rs.error_code == '0') & rs.next():
                        # 获取一条记录，将记录合并在一起
                        data_list.append(rs.get_row_data())
                    result = pd.DataFrame(data_list, columns=rs.fields)
                    is_first = True if step == 1 else False
                    thr = Thread(target=_parse_data, args=[result, task.ts_code, frequency, is_first])  #后台解析数据
                    thr.start()
                    if is_first:
                        thr.join()
                    task.finished = True
                    step += 1
                    break
                elif i < (max_try - 1):
                    time.sleep(2)
                    continue
                else:
                    _logger.error('query_history_k_data_plus respond error_code:' + rs.error_code)
                    _logger.error('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        sm.commit()
    #### 登出系统 ####
    bs.logout()


def init_history_k_data_plus(frequency, adjustflag="3"):
    """
    初始化历史K线数据
    """
    fields = frequency_fields[frequency]
    _query_history_k_data_plus(fields, frequency, adjustflag)
