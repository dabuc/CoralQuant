# -*- coding: utf-8 -*-
"""
操作数据层数据模型，用于保存原始数据
"""
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, BigInteger, Numeric, String, Enum, Float, Boolean, Date
from coralquant.database import Base
metadata = MetaData()

stock_basic = Table(
    "odl_ts_stock_basic",
    metadata,
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


class BS_Stock_Basic(Base):
    """
    日线历史行情数据
    """
    __tablename__ = "odl_bs_stock_basic"
    code = Column(String(10), primary_key=True)
    code_name = Column(String(100))
    ipoDate = Column(String(10))
    outDate = Column(String(10))
    type = Column(String(10))
    status = Column(String(10))


def default_t_date(context):

    datestr = context.get_current_parameters()['date']
    t_date = datetime.strptime(datestr, "%Y-%m-%d").date()
    return t_date


class D_History_A_Stock_K_Data(Base):
    """
    日线历史行情数据
    """
    __tablename__ = "odl_d_history_A_stock_k_data"
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', String(10))
    code = Column('code', String(10))
    open = Column('open', String(15))
    high = Column('high', String(15))
    low = Column('low', String(15))
    close = Column('close', String(15))
    preclose = Column('preclose', String(15))
    volume = Column('volume', String(20))
    amount = Column('amount', String(23))
    adjustflag = Column('adjustflag', String(1))
    turn = Column('turn', String(15))
    tradestatus = Column('tradestatus', String(1))
    pctChg = Column('pctChg', String(15))
    peTTM = Column('peTTM', String(20))
    pbMRQ = Column('pbMRQ', String(20))
    psTTM = Column('psTTM', String(20))
    pcfNcfTTM = Column('pcfNcfTTM', String(20))
    isST = Column('isST', String(1))
    t_date = Column('t_date', Date, default=default_t_date)


class W_History_A_Stock_K_Data(Base):
    """
    周线历史行情数据
    """
    __tablename__ = "odl_w_history_A_stock_k_data"
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', String(10))
    code = Column('code', String(10))
    open = Column('open', String(15))
    high = Column('high', String(15))
    low = Column('low', String(15))
    close = Column('close', String(15))
    volume = Column('volume', String(20))
    amount = Column('amount', String(23))
    adjustflag = Column('adjustflag', String(1))
    turn = Column('turn', String(15))
    pctChg = Column('pctChg', String(15))
    t_date = Column('t_date', Date, default=default_t_date)


class M_History_A_Stock_K_Data(Base):
    """
    月线历史行情数据
    """
    __tablename__ = "odl_m_history_A_stock_k_data"
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', String(10))
    code = Column('code', String(10))
    open = Column('open', String(15))
    high = Column('high', String(15))
    low = Column('low', String(15))
    close = Column('close', String(15))
    volume = Column('volume', String(20))
    amount = Column('amount', String(23))
    adjustflag = Column('adjustflag', String(1))
    turn = Column('turn', String(15))
    pctChg = Column('pctChg', String(15))
    t_date = Column('t_date', Date, default=default_t_date)


class T5_History_A_Stock_K_Data(Base):
    """
    5分钟线历史行情数据
    """
    __tablename__ = "odl_t5_history_A_Stock_K_Data"
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', String(10))
    time = Column('time', String(10))
    code = Column('code', String(10))
    open = Column('open', String(15))
    high = Column('high', String(15))
    low = Column('low', String(15))
    close = Column('close', String(15))
    volume = Column('volume', String(20))
    amount = Column('amount', String(23))
    adjustflag = Column('adjustflag', String(1))


if __name__ == "__main__":
    pass