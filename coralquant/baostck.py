import random
import time

import baostock as bs
import pandas as pd
from sqlalchemy import create_engine, select

from coralquant import logger
from coralquant.models.odl_model import stock_basic
from coralquant.settings import CQ_Config

engine = create_engine(CQ_Config.DATABASE_URL)
connection = engine.connect()

def get_task_list():
    """
    获取股票列表
    """
    s = select([stock_basic.c.ts_code
                ]).where(stock_basic.c.list_status == 'L')
    rp = connection.execute(s)
    task_list = []
    for row in rp:
        a = row[0].split('.')
        code = '{}.{}'.format(a[1].lower(), a[0])
        iscmpl = False
        task = [code, iscmpl]
        task_list.append(task)
    return task_list


def init_history_k_data_plus():
    """
    初始化日线数据
    """
    _logger = logger.Logger(__name__).get_log()

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    _logger.info("login respond error_code:" + lg.error_code)
    _logger.info("login respond  error_msg:" + lg.error_msg)


    task_list= get_task_list()
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
                "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                start_date='1990-12-19',
                end_date='2020-10-11',
                frequency="d",
                adjustflag="3",
            )  # frequency="d"取日k线，adjustflag="3"默认不复权
            _logger.info("query_history_k_data_plus respond error_code:" +
                        rs.error_code)
            _logger.info("query_history_k_data_plus respond  error_msg:" +
                        rs.error_msg)

            #### 打印结果集 ####
            data_list = []
            while (rs.error_code == "0") & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            
            result.to_sql('tmp_history_A_stock_k_data',
                        connection,
                        schema='stock_dw',
                        if_exists='replace' if step == 1 else 'append',
                        index=False)
            step += 1
        except Exception as e:
            _logger.error("{}下载失败,no.{}".format(task[0], step))
        else:
            task[1] = True
            _logger.info("完成{}下载,no.{}".format(task[0], step))


    #### 登出系统 ####
    bs.logout()
