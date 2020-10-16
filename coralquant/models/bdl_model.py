# -*- coding: utf-8 -*-
"""
基础数据层数据模型
"""
from datetime import datetime

from coralquant.database import Base
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, MetaData,
                        Numeric, String, Table)



class DailyKData(Base):
    """
    日线数据
    """
    __tablename__ = "bdl_bs_daily_k_data"
    id = Column( BigInteger, primary_key=True)
    date = Column( Date, nullable=False)  #交易所行情日期
    code = Column( String(10), nullable=False)  #证券代码
    open = Column('open', Numeric(12, 4), nullable=False)  #今开盘价格
    high = Column('high', Numeric(12, 4), nullable=False)  #最高价
    low = Column('low', Numeric(12, 4), nullable=False)  #最低价
    close = Column('close', Numeric(12, 4), nullable=False)  #今收盘价
    preclose = Column('preclose', Numeric(12, 4), nullable=False)  #昨日收盘价
    volume = Column('volume', BigInteger, nullable=False)  #成交数量
    amount = Column('amount', Numeric(23, 4), nullable=False)  #成交金额
    adjustflag = Column('adjustflag', Enum('1', '2', '3'), nullable=False)  #复权状态
    turn = Column('turn', Float, nullable=False)  #换手率
    tradestatus = Column('tradestatus', Boolean, nullable=False)  #交易状态
    pctChg = Column('pctChg', Float, nullable=False)  #涨跌幅（百分比）
    peTTM = Column('peTTM', Float, nullable=False)  #滚动市盈率
    pbMRQ = Column('pbMRQ', Float, nullable=False)  #滚动市销率
    psTTM = Column('psTTM', Float, nullable=False)  #滚动市现率
    pcfNcfTTM = Column('pcfNcfTTM', Float, nullable=False)  #市净率
    isST = Column('isST', Boolean, nullable=False)  #是否ST


class WeeklyKData(Base):
    """
    周线数据
    """
    __tablename__ = "bdl_bs_weekly_k_data"
    id = Column( BigInteger, primary_key=True)
    date = Column('date', Date, nullable=False)  #交易所行情日期
    code = Column('code', String(10), nullable=False)  #证券代码
    open = Column('open', Numeric(12, 4), nullable=False)  #今开盘价格
    high = Column('high', Numeric(12, 4), nullable=False)  #最高价
    low = Column('low', Numeric(12, 4), nullable=False)  #最低价
    close = Column('close', Numeric(12, 4), nullable=False)  #今收盘价
    volume = Column('volume', BigInteger, nullable=False)  #成交数量
    amount = Column('amount', Numeric(23, 4), nullable=False)  #成交金额
    adjustflag = Column('adjustflag', Enum('1', '2', '3'), nullable=False)  #复权状态
    turn = Column('turn', Float, nullable=False)  #换手率
    pctChg = Column('pctChg', Float, nullable=False)  #涨跌幅（百分比）


class MonthlyKData(Base):
    """
    月线数据
    """
    __tablename__ = "bdl_bs_monthly_k_data"
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', Date, nullable=False)  #交易所行情日期
    code = Column('code', String(10), nullable=False)  #证券代码
    open = Column('open', Numeric(12, 4), nullable=False)  #今开盘价格
    high = Column('high', Numeric(12, 4), nullable=False)  #最高价
    low = Column('low', Numeric(12, 4), nullable=False)  #最低价
    close = Column('close', Numeric(12, 4), nullable=False)  #今收盘价
    volume = Column('volume', BigInteger, nullable=False)  #成交数量
    amount = Column('amount', Numeric(23, 4), nullable=False)  #成交金额
    adjustflag = Column('adjustflag', Enum('1', '2', '3'), nullable=False)  #复权状态
    turn = Column('turn', Float, nullable=False)  #换手率
    pctChg = Column('pctChg', Float, nullable=False)  #涨跌幅（百分比）


if __name__ == "__main__":
    pass
