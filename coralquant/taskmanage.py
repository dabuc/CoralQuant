# -*- coding: utf-8 -*-
from coralquant import logger
from datetime import date
from sqlalchemy import MetaData, Table, insert, select
from coralquant.database import engine
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import session_maker,TaskTable
from coralquant.stringhelper import TaskEnum

_logger = logger.Logger(__name__).get_log()

meta = MetaData()

def update_task_table():
    """
    更新任务表
    """
    pass


def create_task(task: int, begin_date: date, end_date: date, codes: list = [], type: str = None, status: str = None,isdel=False):
    """
    创建任务

    type：证券类型，其中1：股票，2：指数,3：其它

    status：上市状态，其中1：上市，0：退市
    """
    try:
        taskEnum= TaskEnum(task)
    except Exception as e:
        _logger.info('指定的任务不存在，创建任务表失败！')
        return
    
     



    if not codes:
        tmp = Table('odl_bs_stock_basic', meta, autoload=True, autoload_with=engine)
        s = select([tmp.c.code])
        if status:
            s = s.where(tmp.c.status == status)
        if type:
            s = s.where(tmp.c.type == type)
        
        #print(str(s))

        codes = engine.execute(s).fetchall()

    tasklist=[]
    with session_maker() as sm:
        if isdel:
            #删除原有的相同任务的历史任务列表
            query= sm.query(TaskTable).filter(TaskTable.task==task)
            query.delete()
            sm.commit()
            _logger.info('{}-历史任务已删除'.format(task))
        
        for c in codes:
            tasktable= TaskTable(
                task=task,
                task_name= taskEnum.name,
                ts_code=c.code,
                begin_date=begin_date,
                end_date=end_date
            )
            tasklist.append(tasktable)
        sm.bulk_save_objects(tasklist)
    
    _logger.info('生成{}条任务记录'.format(len(codes)))



    if __name__ == "__main__":
        pass
