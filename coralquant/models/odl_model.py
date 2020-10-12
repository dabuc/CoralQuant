# -*- coding: utf-8 -*-
"""
操作数据层数据模型，用于保存原始数据
"""
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, Numeric, String, Enum, Float, Boolean,Date

odl_metadata = MetaData()

stock_basic = Table(
    "odl_ts_stock_basic",
    odl_metadata,
    Column("ts_code", String(10)),  # TS代码
    Column("symbol", String(6), primary_key=True),  # 股票代码
    Column("name", String(10)),  # 股票名称
    Column("area", String(4)),  # 所在地域
    Column("industry", String(4)),  # 所属行业
    Column("fullname", String(25)),  # 股票全称
    Column("enname", String(100)),  # 英文全称
    Column("market", String(3)),  # 市场类型 （主板/中小板/创业板/科创板）
    Column("exchange", String(4), nullable=False),  # 交易所代码
    Column("curr_type", String(3)),  # 交易货币
    Column("list_status", String(1), nullable=False),  # 上市状态： L上市 D退市 P暂停上市
    Column("list_date", String(8)),  # 上市日期
    Column("delist_date", String(8)),  # 退市日期
    Column("is_hs", String(1), nullable=False),  # 是否沪深港通标的，N否 H沪股通 S深股通
)

daily_k_data = Table(
    "odl_bs_daily_k_data",
    odl_metadata,
    Column('date', Date, nullable=False),  #交易所行情日期	
    Column('code', String(10), nullable=False),  #证券代码
    Column('open', Numeric(12, 4), nullable=False),  #今开盘价格
    Column('high', Numeric(12, 4), nullable=False),  #最高价
    Column('low', Numeric(12, 4), nullable=False),  #最低价
    Column('close', Numeric(12, 4), nullable=False),  #今收盘价
    Column('preclose', Numeric(12, 4), nullable=False),  #昨日收盘价
    Column('volume', Integer, nullable=False),  #成交数量
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


if __name__ == "__main__":
    pass