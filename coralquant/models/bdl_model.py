# -*- coding: utf-8 -*-
"""
基础数据层数据模型
"""
from sqlalchemy import Table, Column, Integer, BigInteger, Numeric, String, Enum, Float, Boolean, Date
from coralquant.models import metadata


daily_k_data = Table(
    "bdl_bs_daily_k_data",
    metadata,
    Column('date', Date, nullable=False),  #交易所行情日期	
    Column('code', String(10), nullable=False),  #证券代码
    Column('open', Numeric(12, 4), nullable=False),  #今开盘价格
    Column('high', Numeric(12, 4), nullable=False),  #最高价
    Column('low', Numeric(12, 4), nullable=False),  #最低价
    Column('close', Numeric(12, 4), nullable=False),  #今收盘价
    Column('preclose', Numeric(12, 4), nullable=False),  #昨日收盘价
    Column('volume', BigInteger, nullable=False),  #成交数量
    Column('amount', Numeric(23, 4), nullable=False),  #成交金额
    Column('adjustflag', Enum('1', '2', '3'), nullable=False),  #复权状态
    Column('turn', Float, nullable=False),  #换手率
    Column('tradestatus', Boolean, nullable=False),  #交易状态
    Column('pctChg', Float, nullable=False),  #涨跌幅（百分比）
    Column('peTTM', Float, nullable=False),  #滚动市盈率
    Column('pbMRQ', Float, nullable=False),  #滚动市销率
    Column('psTTM', Float, nullable=False),  #滚动市现率
    Column('pcfNcfTTM', Float, nullable=False),  #市净率
    Column('isST', Boolean, nullable=False)  #是否ST
)

weekly_k_data = Table(
    "bdl_bs_weekly_k_data",
    metadata,
    Column('date', Date, nullable=False),  #交易所行情日期	
    Column('code', String(10), nullable=False),  #证券代码
    Column('open', Numeric(12, 4), nullable=False),  #今开盘价格
    Column('high', Numeric(12, 4), nullable=False),  #最高价
    Column('low', Numeric(12, 4), nullable=False),  #最低价
    Column('close', Numeric(12, 4), nullable=False),  #今收盘价
    Column('volume', BigInteger, nullable=False),  #成交数量
    Column('amount', Numeric(23, 4), nullable=False),  #成交金额
    Column('adjustflag', Enum('1', '2', '3'), nullable=False),  #复权状态
    Column('turn', Float, nullable=False),  #换手率
    Column('pctChg', Float, nullable=False),  #涨跌幅（百分比）
)

monthly_k_data = Table(
    "bdl_bs_monthly_k_data",
    metadata,
    Column('date', Date, nullable=False),  #交易所行情日期	
    Column('code', String(10), nullable=False),  #证券代码
    Column('open', Numeric(12, 4), nullable=False),  #今开盘价格
    Column('high', Numeric(12, 4), nullable=False),  #最高价
    Column('low', Numeric(12, 4), nullable=False),  #最低价
    Column('close', Numeric(12, 4), nullable=False),  #今收盘价
    Column('volume', BigInteger, nullable=False),  #成交数量
    Column('amount', Numeric(23, 4), nullable=False),  #成交金额
    Column('adjustflag', Enum('1', '2', '3'), nullable=False),  #复权状态
    Column('turn', Float, nullable=False),  #换手率
    Column('pctChg', Float, nullable=False),  #涨跌幅（百分比）
)
