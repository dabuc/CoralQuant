# -*- coding: utf-8 -*-
"""
定义sqlalchemy的全局对象
"""
from datetime import datetime
from coralquant.database import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import Table, Column, Integer, String, Date, Float, DateTime, Boolean, UniqueConstraint
from coralquant.settings import CQ_Config

Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


@contextmanager
def session_maker(session=session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


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