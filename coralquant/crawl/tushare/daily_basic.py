"""每日指标
"""
import concurrent.futures
from datetime import datetime
from coralquant.stringhelper import TaskEnum
from coralquant.models.orm_model import TaskTable
import time
from tqdm import tqdm
from coralquant.models.odl_model import TS_Daily_Basic, TS_Stock_Basic
from coralquant.database import engine, session_scope, del_table_data
import tushare as ts
from coralquant.settings import CQ_Config
from dateutil.parser import parse
from coralquant import logger
from sqlalchemy import String
from coralquant.database import get_new_session

_logger = logger.Logger(__name__).get_log()


def _parse_data(content, task_date):
    """
    解析数据，并保存
    """

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
    taskEnum = TaskEnum.TS更新每日指标

    with concurrent.futures.ThreadPoolExecutor() as executor:

        sm = get_new_session()
        try:
            rp = sm.query(TaskTable).filter(TaskTable.task == taskEnum.value, TaskTable.finished == False)

            if CQ_Config.IDB_DEBUG == '1':  #如果是测试环境
                rp = rp.limit(10)

            rp = rp.all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                max_try = 8  # 失败重连的最大次数
                for i in range(max_try):
                    try:
                        tasktime = datetime.strftime(task.begin_date, '%Y%m%d')
                        result = pro_api.daily_basic(trade_date=tasktime, fields=fields)
                        executor.submit(_parse_data, result, task.begin_date)
                        task.finished = True
                        time.sleep(0.2)
                        break
                    except Exception as e:
                        if i < (max_try - 1):
                            t = (i + 1) * 2
                            time.sleep(t)
                            _logger.error('[{}]异常重连/{}'.format(task.ts_code, repr(e)))
                            continue
                        else:
                            _logger.error('获取[{}]每日指标失败/{}'.format(task.ts_code, repr(e)))
                            raise
                sm.commit()
        except:
            sm.commit()
            raise
        finally:
            sm.close()
