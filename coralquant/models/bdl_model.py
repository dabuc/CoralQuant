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
    id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False)  #交易所行情日期
    code = Column(String(10), nullable=False)  #证券代码
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
    id = Column(BigInteger, primary_key=True)
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


class quarterly_Profit_Data(Base):
    """
    季频盈利能力
    """
    __tablename__ = "bdl_bs_profit_data"
    id = Column('id', BigInteger, primary_key=True)
    code = Column('code', String(10), nullable=False)  #证券代码
    pubDate = Column('pubDate', Date, nullable=False)  #公司发布财报的日期
    statDate = Column('statDate', Date, nullable=False)  #财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    roeAvg = Column('roeAvg', Numeric(15, 6), nullable=False)  #净资产收益率(平均)(%)
    npMargin = Column('npMargin', Numeric(15, 6), nullable=False)  #销售净利率(%)
    gpMargin = Column('gpMargin', Numeric(15, 6), nullable=False)  #销售毛利率(%)
    netProfit = Column('netProfit', Numeric(23, 6), nullable=False)  #净利润(元)
    epsTTM = Column('epsTTM', Numeric(15, 6), nullable=False)  #每股收益
    MBRevenue = Column('MBRevenue', Numeric(23, 6), nullable=False)  #主营营业收入(元)
    totalShare = Column('totalShare', Numeric(23, 2), nullable=False)  #总股本
    liqaShare = Column('liqaShare', Numeric(23, 2), nullable=False)  #流通股本


if __name__ == "__main__":
    pass
