# -*- coding: utf-8 -*-
"""
日线行情
"""
from coralquant import logger
from coralquant.models.odl_model import TS_Daily
from coralquant.settings import CQ_Config
from coralquant.odl.tushare.util import extract_data
from coralquant.stringhelper import TaskEnum
from coralquant.taskmanage import create_ts_cal_task
import tushare as ts
from dateutil.parser import parse
from sqlalchemy import String
from coralquant.database import engine



_logger = logger.Logger(__name__).get_log()

def update_task():
    """
    更新任务列表
    """
    create_ts_cal_task(TaskEnum.TS日线行情)


def get_daily():
    """
    获取日线行情
    """

    pro_api = ts.pro_api(CQ_Config.TUSHARE_TOKEN)
    pro_api_func = pro_api.daily
    extract_data(
        TaskEnum.TS日线行情,
        pro_api_func,
        {},
        _load_data,
        {},
        '日线行情'
    )


def _load_data(dic:dict):
    """
    做一些简单转换后，加载数据到数据库
    """

    content=dic['result']
    task_date=dic['task_date']

    table_name = TS_Daily.__tablename__

    if content.empty:
        return

    try:
        content['trade_date'] = [parse(x).date() for x in content.trade_date]
        dtype = {'ts_code': String(10)}

        content.to_sql(table_name, engine, schema=CQ_Config.DB_SCHEMA, if_exists='append', index=False, dtype=dtype)
    except Exception as e:
        _logger.error('{}-日线行情保存出错/{}'.format(task_date, repr(e)))