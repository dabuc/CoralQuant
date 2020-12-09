"""每日指标
"""
import concurrent.futures
from coralquant.stringhelper import TaskEnum
from coralquant.models.orm_model import TaskTable
import time
from tqdm import tqdm
from coralquant.models.odl_model import TS_Stock_Basic
from coralquant.database import engine, session_scope, del_table_data
import tushare as ts
from coralquant.settings import CQ_Config
from dateutil.parser import parse
from coralquant import logger
from sqlalchemy import String

_logger = logger.Logger(__name__).get_log()



def _parse_data(content, ts_code, isFirst):
    """
    解析数据，并保存
    """

    table_name = 'odl_ts_daily_basic'

    if content.empty:
        return

    try:
        content['trade_date'] = [parse(x).date() for x in content.trade_date]
        dtype = {'ts_code': String(10)}

        if isFirst:
            if_exists = 'replace'
        else:
            if_exists = 'append'
        content.to_sql(table_name, engine, schema='stock_dw', if_exists=if_exists, index=False, dtype=dtype)
    except Exception as e:
        _logger.error('{}-每日指标更新出错/{}'.format(ts_code, repr(e)))


def update_daily_basic():
    """
    更新每日指标
    """
    pro_api = ts.pro_api(CQ_Config.TUSHARE_TOKEN)
    fields = 'ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,dv_ratio,dv_ttm,total_share,float_share,free_share,total_mv,circ_mv'
    isFirst = True
    taskEnum=TaskEnum.TS更新每日指标

    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as sm:
            rp = sm.query(TaskTable).filter(TaskTable.task == taskEnum.value, TaskTable.finished == False)

            if CQ_Config.IDB_DEBUG == '1':  #如果是测试环境
                rp = rp.limit(10)

            rp = rp.all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                result = pro_api.daily_basic(ts_code=task.ts_code, fields=fields)
                executor.submit(_parse_data, result, task.ts_code, isFirst)
                task.finished = True
                time.sleep(0.3)
                if isFirst:
                    isFirst = False
                    time.sleep(1)
