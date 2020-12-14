"""
计算指定日期往后的5日，10日，20日，60日，120日，250日涨跌幅
"""

import datetime
from datetime import datetime as dtime

from pandas.core.frame import DataFrame

from coralquant import logger
from coralquant.database import session_scope
from coralquant.models.bdl_model import BS_LaterNPctChg
from coralquant.models.odl_model import BS_Daily_hfq
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.util.dataconvert import convert_to_tscode
from sqlalchemy import and_, func, select, distinct, desc
from coralquant.database import engine
import pandas as pd
import numpy as np
from tqdm import tqdm
import concurrent.futures

_logger = logger.Logger(__name__).get_log()


def update_task():
    """
    更新“BS计算指定日期往后N日涨跌幅”任务列表
    """
    # select a.code,min(a.date) mi_date from  odl_bs_daily_hfq a left join bdl_bs_ln_pctchg b on a.code = b.code and a.date=b.date
    # where b.l250_pctChg is null
    # group by a.code

    TaskTable.del_with_task(TaskEnum.BS计算指定日期往后N日涨跌幅)

    with session_scope() as sm:
        #获取所有需要插入的数据
        query = sm.query(distinct(BS_Daily_hfq.code).label('code')).join(
            BS_LaterNPctChg,
            and_(BS_Daily_hfq.code == BS_LaterNPctChg.code, BS_Daily_hfq.date == BS_LaterNPctChg.date),
            isouter=True)
        query = query.filter(BS_LaterNPctChg.code == None)

        codes = query.all()

        tasklist = []
        for c in codes:
            tasktable = TaskTable(task=TaskEnum.BS计算指定日期往后N日涨跌幅.value,
                                  task_name=TaskEnum.BS计算指定日期往后N日涨跌幅.name,
                                  ts_code=convert_to_tscode(c.code),
                                  bs_code=c.code,
                                  begin_date=dtime.strptime('1990-12-19', '%Y-%m-%d').date(),
                                  end_date=dtime.now().date(),
                                  remark='INSERT')
            tasklist.append(tasktable)
        _logger.info('生成{}条任务记录(INSERT)'.format(len(codes)))

        #获取所有需要更新的数据
        query = sm.query(BS_LaterNPctChg.code, func.min(BS_LaterNPctChg.date).label('mi_date'))
        query = query.filter(BS_LaterNPctChg.l250_pctChg == None)
        query = query.group_by(BS_LaterNPctChg.code)
        codes2 = query.all()

        for c in codes2:
            tasktable = TaskTable(task=TaskEnum.BS计算指定日期往后N日涨跌幅.value,
                                  task_name=TaskEnum.BS计算指定日期往后N日涨跌幅.name,
                                  ts_code=convert_to_tscode(c.code),
                                  bs_code=c.code,
                                  begin_date=c.mi_date,
                                  end_date=dtime.now().date(),
                                  remark='UPDATE')
            tasklist.append(tasktable)

        sm.bulk_save_objects(tasklist)
    _logger.info('生成{}条任务记录(UPDATE)'.format(len(codes2)))


def _calc_n_pctChg(df, n: int):
    """
    计算往后N日涨跌幅
    """
    ln_pctChg = 'l{}_pctChg'.format(n)
    tmp = df['close'].shift(-n)
    df[ln_pctChg] = ((tmp - df['close']) / df['close'])  #.round(6)


def calc_later_n_pctChg():
    """
    计算股票往后的5日，10日，20日，60日，120日，250日涨跌幅
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as sm:
            rp = sm.query(TaskTable).filter(TaskTable.task == TaskEnum.BS计算指定日期往后N日涨跌幅.value,
                                            TaskTable.finished == False).all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                s = select([
                    BS_Daily_hfq.id, BS_Daily_hfq.date, BS_Daily_hfq.code, BS_Daily_hfq.close, BS_Daily_hfq.pctChg
                ]).where(and_(BS_Daily_hfq.code == task.bs_code,
                              BS_Daily_hfq.date >= task.begin_date)).order_by(desc(BS_Daily_hfq.date))

                df = pd.read_sql(s, engine)
                _calc_n_pctChg(df, 5)
                _calc_n_pctChg(df, 10)
                _calc_n_pctChg(df, 20)
                _calc_n_pctChg(df, 60)
                _calc_n_pctChg(df, 120)
                _calc_n_pctChg(df, 250)
                #nan can not be used with MySQL
                executor.submit(_load_data, df, task.bs_code, task.remark)
                #_load_data(df,task.bs_code, task.remark)
                task.finished = True
            sm.commit()


def _load_data(df: DataFrame, bs_code, remark):
    """
    更新 BS_LaterNPctChg 数据表
    """

    with session_scope() as sm:
        if remark == 'INSERT':
            laterNPctChglist=[]
            for i in df.itertuples():
                laterNPctChg = BS_LaterNPctChg(code=i.code,
                                        date=i.date,
                                        pctChg=_set_pctChg(i.pctChg) ,
                                        l5_pctChg=_set_pctChg(i.l5_pctChg),
                                        l10_pctChg=_set_pctChg(i.l10_pctChg),
                                        l20_pctChg=_set_pctChg(i.l20_pctChg),
                                        l60_pctChg=_set_pctChg(i.l60_pctChg),
                                        l120_pctChg=_set_pctChg(i.l120_pctChg),
                                        l250_pctChg=_set_pctChg(i.l250_pctChg))
                laterNPctChglist.append(laterNPctChg)
            sm.bulk_save_objects(laterNPctChglist)
            sm.commit()
        else:
            rq = sm.query(BS_LaterNPctChg).filter(BS_LaterNPctChg.code == bs_code)
            rq = rq.filter(BS_LaterNPctChg.l250_pctChg == None)
            for row in rq:
                for i in df.itertuples():
                    if row.code == i.code and row.date == i.date:
                        row.l5_pctChg = _set_pctChg(i.l5_pctChg)
                        row.l10_pctChg = _set_pctChg(i.l10_pctChg)
                        row.l20_pctChg = _set_pctChg(i.l20_pctChg)
                        row.l60_pctChg = _set_pctChg(i.l60_pctChg)
                        row.l120_pctChg = _set_pctChg(i.l120_pctChg)
                        row.l250_pctChg = _set_pctChg(i.l250_pctChg)
            sm.commit()

def _set_pctChg(pctChg):
    if pd.isnull(pctChg):
        return None
    else:
        return pctChg
