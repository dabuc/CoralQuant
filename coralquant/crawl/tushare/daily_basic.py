"""每日指标
"""
import concurrent.futures
from coralquant.crawl.tushare.util import extract_data
from datetime import datetime
from coralquant.stringhelper import TaskEnum
from coralquant.models.orm_model import TaskTable
import time
from tqdm import tqdm
from coralquant.models.odl_model import TS_Daily_Basic
from coralquant.database import engine
import tushare as ts
from coralquant.settings import CQ_Config
from dateutil.parser import parse
from coralquant import logger
from sqlalchemy import String
from coralquant.database import get_new_session

_logger = logger.Logger(__name__).get_log()


def _parse_data(dic: dict):
    """
    解析数据，并保存
    """

    content = dic['result']
    task_date = dic['task_date']

    table_name = TS_Daily_Basic.__tablename__

    if content.empty:
        return

    try:
        content['trade_date'] = [parse(x).date() for x in content.trade_date]
        dtype = {'ts_code': String(10)}

        content.to_sql(table_name, engine, schema='stock_dw', if_exists='append', index=False, dtype=dtype)
    except Exception as e:
        _logger.error('{}-每日指标更新出错/{}'.format(task_date, repr(e)))


def update_daily_basic():
    """
    更新每日指标
    """
    pro_api = ts.pro_api(CQ_Config.TUSHARE_TOKEN)
    fields = 'ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,dv_ratio,dv_ttm,total_share,float_share,free_share,total_mv,circ_mv'
    pro_api_func = pro_api.daily_basic
    extract_data(TaskEnum.TS更新每日指标, pro_api_func, {'fields': fields}, _parse_data, {}, '每日指标')
