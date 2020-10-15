# -*- coding: utf-8 -*-
"""
定义sqlalchemy的全局对象
"""
from datetime import datetime

from coralquant.database import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, Integer,
                        String, Table, UniqueConstraint)


class TaskTable(Base):
    """
    任务配置表
    """
    __tablename__ = "bdl_task_table"
    id = Column(Integer, primary_key=True)
    task = Column(Integer, nullable=False)  #任务ID
    task_name = Column(String(30), nullable=False)  #任务
    ts_code = Column(String(10), nullable=False)  #证券代码 bs格式
    begin_date = Column(Date, nullable=False)  #开始时间
    end_date = Column(Date, nullable=False)  #结束时间
    finished = Column(Boolean, default=False, nullable=False)  #是否完成
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


if __name__ == "__main__":
    pass
