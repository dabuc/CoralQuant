# -*- coding: utf-8 -*-
from coralquant.models.odl_model import BS_Stock_Basic, BS_SZ50_Stocks, TS_Stock_Basic, TS_TradeCal
from coralquant.spider.bs_stock_basic import get_stock_basic
from coralquant import logger
from datetime import date, datetime, timedelta
from sqlalchemy import MetaData
from coralquant.database import session_scope
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from sqlalchemy import func, distinct

_logger = logger.Logger(__name__).get_log()

meta = MetaData()


def create_task(
    task: TaskEnum,
    begin_date: date,
    end_date: date,
    codes: list = [],
    type: str = None,
    status: str = None,
    market: str = None,
    isdel=False,
):
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
            query = sm.query(BS_Stock_Basic.code, BS_Stock_Basic.ipoDate)
            if market:
                query = query.join(TS_Stock_Basic, BS_Stock_Basic.code == TS_Stock_Basic.bs_code).filter(
                    TS_Stock_Basic.market == market
                )
            if CQ_Config.IDB_DEBUG == "1":  # 如果是测试环境
                query = query.join(BS_SZ50_Stocks, BS_Stock_Basic.code == BS_SZ50_Stocks.code)
            if status:
                query = query.filter(BS_Stock_Basic.status == status)
            if type:
                query = query.filter(BS_Stock_Basic.type == type)
            codes = query.all()

        if isdel:
            # 删除原有的相同任务的历史任务列表
            query = sm.query(TaskTable).filter(TaskTable.task == task.value)
            query.delete()
            sm.commit()
            _logger.info("任务：{}-历史任务已删除".format(task.name))

        tasklist = []
        for c in codes:
            tasktable = TaskTable(
                task=task.value,
                task_name=task.name,
                ts_code=c.code,
                begin_date=begin_date if begin_date is not None else c.ipoDate,
                end_date=end_date,
            )
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)

    _logger.info("生成{}条任务记录".format(len(codes)))


def create_bs_task(task: TaskEnum, tmpcodes=None):
    """
    创建BS任务列表
    """
    # 删除原有的相同任务的历史任务列表
    TaskTable.del_with_task(task)

    with session_scope() as sm:
        query = sm.query(BS_Stock_Basic.code, BS_Stock_Basic.ipoDate, BS_Stock_Basic.outDate, BS_Stock_Basic.ts_code)
        if CQ_Config.IDB_DEBUG == "1":  # 如果是测试环境
            if tmpcodes:
                query = query.filter(BS_Stock_Basic.code.in_(tmpcodes))
            else:
                query = query.join(BS_SZ50_Stocks, BS_Stock_Basic.code == BS_SZ50_Stocks.code)
        # query = query.filter(BS_Stock_Basic.status == True)  #取上市的

        codes = query.all()

        tasklist = []
        for c in codes:
            tasktable = TaskTable(
                task=task.value,
                task_name=task.name,
                ts_code=c.ts_code,
                bs_code=c.code,
                begin_date=c.ipoDate,
                end_date=c.outDate if c.outDate is not None else datetime.now().date(),
            )
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)
    _logger.info("生成{}条任务记录".format(len(codes)))


def create_ts_task(task: TaskEnum):
    """
    创建TS任务列表
    """
    # 删除原有的相同任务的历史任务列表
    TaskTable.del_with_task(task)

    with session_scope() as sm:

        codes = (
            sm.query(
                TS_Stock_Basic.ts_code, TS_Stock_Basic.bs_code, TS_Stock_Basic.list_date, TS_Stock_Basic.delist_date
            )
            .filter(TS_Stock_Basic.list_status == "L")
            .all()
        )

        tasklist = []
        for c in codes:
            tasktable = TaskTable(
                task=task.value,
                task_name=task.name,
                ts_code=c.ts_code,
                bs_code=c.bs_code,
                begin_date=c.list_date,
                end_date=c.delist_date if c.delist_date is not None else datetime.now().date(),
            )
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)
    _logger.info("生成{}条任务记录".format(len(codes)))


def create_ts_cal_task(task: TaskEnum):
    """
    创建基于交易日历的任务列表
    """
    # 删除历史任务
    TaskTable.del_with_task(task)

    with session_scope() as sm:
        rp = sm.query(distinct(TS_TradeCal.date).label("t_date")).filter(
            TS_TradeCal.is_open == True, TS_TradeCal.date <= datetime.now().date()  # noqa
        )
        codes = rp.all()
        tasklist = []
        for c in codes:
            tasktable = TaskTable(
                task=task.value,
                task_name=task.name,
                ts_code="按日期更新",
                bs_code="按日期更新",
                begin_date=c.t_date,
                end_date=c.t_date,
            )
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)
    _logger.info("生成{}条任务记录".format(len(codes)))


if __name__ == "__main__":
    pass
