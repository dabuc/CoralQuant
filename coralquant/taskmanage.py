# -*- coding: utf-8 -*-
from coralquant.models.odl_model import BS_Stock_Basic, TS_Stock_Basic
from coralquant.spider.bs_stock_basic import get_stock_basic
from coralquant import logger
from datetime import date, datetime, timedelta
from sqlalchemy import MetaData, Table, insert, select
from coralquant.database import engine, session_scope
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum, frequency_bdl_table_obj
from sqlalchemy.sql import func

_logger = logger.Logger(__name__).get_log()

meta = MetaData()




def update_task_table(task: TaskEnum, market: str = None):
    """
    更新任务表
        1.获取最新bs-A股股票列表
        2.创建任务表
        3.根据依据导入的数据，更新任务表时间
    """
    get_stock_basic()

    begin_date = datetime.strptime('1990-12-19', "%Y-%m-%d").date()
    end_date = datetime.now().date()

    create_task(task, begin_date, end_date, type='1', market=market, isdel=True)  #股票
    if not market:
        create_task(task, begin_date, end_date, type='2')  #指数

    tbl = frequency_bdl_table_obj[task.value]
    with session_scope() as sn:
        rq = sn.query(tbl.code, func.max(tbl.date).label('m_date')).group_by(tbl.code).all()
        task_query = sn.query(TaskTable).filter(TaskTable.task == task.value).all()

        for row in rq:

            for taskrow in task_query:
                if taskrow.ts_code == row.code:
                    taskrow.begin_date = row.m_date + timedelta(1)

    _logger.info('任务表更新完成')


def create_task(task: TaskEnum,
                begin_date: date,
                end_date: date,
                codes: list = [],
                type: str = None,
                status: str = None,
                market: str = None,
                isdel=False):
    """创建任务

    :param task: 任务类型
    :type task: TaskEnum
    :param begin_date: 如果开始时间(begin_date)为None，开始时间取股票上市(IPO)时间
    :type begin_date: date
    :param end_date: 结束时间
    :type end_date: date
    :param codes: 股票代码列表, defaults to []
    :type codes: list, optional
    :param type: 证券类型，其中1：股票，2：指数,3：其它, defaults to None
    :type type: str, optional
    :param status: 上市状态，其中1：上市，0：退市, defaults to None
    :type status: str, optional
    :param market: 市场类型 （主板/中小板/创业板/科创板/CDR）, defaults to None
    :type market: str, optional
    :param isdel: 是否删除删除原有的相同任务的历史任务列表, defaults to False
    :type isdel: bool, optional
    """                
    
    with session_scope() as sm:
        if not codes:
            query = sm.query(BS_Stock_Basic.code,BS_Stock_Basic.ipoDate)
            if market:
                query = query.join(
                    TS_Stock_Basic,
                    BS_Stock_Basic.code == TS_Stock_Basic.bs_code).filter(TS_Stock_Basic.market == market)
            if status:
                query = query.filter(BS_Stock_Basic.status == status)
            if type:    
                query = query.filter(BS_Stock_Basic.type == type)
            codes = query.all()

        if isdel:
            #删除原有的相同任务的历史任务列表
            query = sm.query(TaskTable).filter(TaskTable.task == task.value)
            query.delete()
            sm.commit()
            _logger.info('任务：{}-历史任务已删除'.format(task.name))

        tasklist = []
        for c in codes:
            tasktable = TaskTable(task=task.value,
                                  task_name=task.name,
                                  ts_code=c.code,
                                  begin_date=begin_date if begin_date is not None else c.ipoDate,
                                  end_date=end_date)
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)

    _logger.info('生成{}条任务记录'.format(len(codes)))




if __name__ == "__main__":
    pass
