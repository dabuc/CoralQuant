# -*- coding: utf-8 -*-
"""
操作数据层数据模型，用于保存原始数据
"""
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, BigInteger, Numeric, String, Enum, Float, Boolean, Date, DateTime
from coralquant.database import Base, session_scope


class BS_Stock_Basic(Base):
    """
    BS-证券基本资料
    """
    __tablename__ = "odl_bs_stock_basic"
    code = Column(String(10), primary_key=True)
    code_name = Column(String(100))
    ipoDate = Column(Date)
    outDate = Column(Date)
    type = Column(String(10))
    status = Column(String(10))
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def del_all_date():
        """
        删除全部数据
        """
        with session_scope() as session:
            session.query(BS_Stock_Basic).delete()


def default_t_date(context):

    datestr = context.get_current_parameters()['date']
    t_date = datetime.strptime(datestr, "%Y-%m-%d").date()
    return t_date


#-------A股K线数据表基类----------

class D_History_A_Stock_K_Data_Base():
    """
    日线历史行情数据
    """
    id = Column('id', BigInteger, primary_key=True)
    date = Column('date', String(10))
    code = Column('code', String(10))
    open = Column('open', String(20))
    high = Column('high', String(20))
    low = Column('low', String(20))
    close = Column('close', String(20))
    preclose = Column('preclose', String(20))
    volume = Column('volume', String(20))
    amount = Column('amount', String(23))
    adjustflag = Column('adjustflag', String(1))#复权状态(1：后复权， 2：前复权，3：不复权）
    turn = Column('turn', String(15))
    tradestatus = Column('tradestatus', String(1))
    pctChg = Column('pctChg', String(15))
    peTTM = Column('peTTM', String(20))
    pbMRQ = Column('pbMRQ', String(20))
    psTTM = Column('psTTM', String(20))
    pcfNcfTTM = Column('pcfNcfTTM', String(20))
    isST = Column('isST', String(1))
    t_date = Column('t_date', Date, default=default_t_date)


class W_History_A_Stock_K_Data_Base():
    """
    周线历史行情数据
    """
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


class M_History_A_Stock_K_Data_Base():
    """
    月线历史行情数据
    """
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


class T5_History_A_Stock_K_Data_Base():
    """
    5分钟线历史行情数据
    """
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

#-------不复权-A股K线数据----------

class D_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base,Base):
    """
    日线历史行情数据
    """
    __tablename__ = "odl_d_history_A_stock_k_data"

class W_History_A_Stock_K_Data(W_History_A_Stock_K_Data_Base,Base):
    """
    周线历史行情数据
    """
    __tablename__ = "odl_w_history_A_stock_k_data"

class M_History_A_Stock_K_Data(M_History_A_Stock_K_Data_Base,Base):
    """
    月线历史行情数据
    """
    __tablename__ = "odl_m_history_A_stock_k_data"


#-------前复权-A股K线数据----------

class D2_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base,Base):
    """
    前复权-日线历史行情数据
    """
    __tablename__ = "odl_d2_history_A_stock_k_data"


#------后复权------------
class D1_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base,Base):
    """
    后复权-日线历史行情数据
    """
    __tablename__ = "odl_d1_history_A_stock_k_data"


class SZ50_Stocks(Base):
    """
    后复权-日线历史行情数据
    """
    __tablename__ = "odl_bs_sz50_stocks"
    id = Column('id', BigInteger, primary_key=True)
    updateDate = Column('updateDate', String(10))
    code = Column('code', String(10))
    code_name = Column('code_name', String(10))

    @staticmethod
    def del_all_data():
        """
        删除数据
        """
        with session_scope() as sn:
            sn.query(SZ50_Stocks).delete()
    




#-------财务数据----------

class Profit_Data(Base):
    """
    季频盈利能力
    """
    __tablename__ = "odl_bs_profit_data"
    id = Column('id', BigInteger, primary_key=True)
    code = Column('code', String(10)) #证券代码	
    pubDate= Column('pubDate', String(10)) #公司发布财报的日期
    statDate= Column('statDate', String(10)) #财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
    roeAvg = Column('roeAvg', String(23)) #净资产收益率(平均)(%)
    npMargin= Column('npMargin', String(23)) #销售净利率(%)
    gpMargin= Column('gpMargin', String(23)) #销售毛利率(%)
    netProfit= Column('netProfit', String(23)) #净利润(元)
    epsTTM= Column('epsTTM', String(23)) #每股收益
    MBRevenue= Column('MBRevenue', String(23)) #主营营业收入(元)
    totalShare= Column('totalShare', String(23)) #总股本
    liqaShare= Column('liqaShare', String(23)) #流通股本



# =========================Tushare数据源模型============================

class TS_Stock_Basic(Base):
    """
    TS-证券基本资料
    """
    __tablename__ = "odl_ts_stock_basic"
    ts_code = Column("ts_code", String(10))  # TS代码
    symbol = Column("symbol", String(6), primary_key=True)  # 股票代码
    name = Column("name", String(10))  # 股票名称
    area = Column("area", String(4))  # 所在地域
    industry = Column("industry", String(4))  # 所属行业
    fullname = Column("fullname", String(25))  # 股票全称
    enname = Column("enname", String(100))  # 英文全称
    market = Column("market", String(3))  # 市场类型 （主板/中小板/创业板/科创板）
    exchange = Column("exchange", String(4), nullable=False)  # 交易所代码
    curr_type = Column("curr_type", String(3))  # 交易货币
    list_status = Column("list_status", String(1), nullable=False)  # 上市状态： L上市 D退市 P暂停上市
    list_date = Column("list_date", Date)  # 上市日期
    delist_date = Column("delist_date", Date)  # 退市日期
    is_hs = Column("is_hs", String(1))  # 是否沪深港通标的，N否 H沪股通 S深股通
    bs_code = Column("bs_code", String(10), index=True)  # BS代码

class TS_Daily_hfq(Base):
    """
    后复权日线行情数据
    """

    __tablename__ = "ods_ts_Daily_hfq"
    id = Column("id", Integer, primary_key=True)
    ts_code = Column("ts_code", String(10), nullable=False)  # 股票代码
    trade_date = Column("trade_date", Date, nullable=False)  # 交易日期
    open = Column("open", Numeric(12, 4), nullable=False)  # 开盘价
    high = Column("high", Numeric(12, 4), nullable=False)  # 最高价
    low = Column("low", Numeric(12, 4), nullable=False)  # 最低价
    close = Column("close", Numeric(12, 4), nullable=False)  # 收盘价
    pre_close = Column("pre_close", Numeric(12, 4), nullable=False)  # 昨收价
    change = Column("change", Numeric(12, 4), nullable=False)  # 涨跌额
    pct_chg = Column("pct_chg", Float, nullable=False)  # 涨跌幅
    vol = Column("vol", Numeric(23, 4), nullable=False)  # 成交量 （手）
    amount = Column("amount", Numeric(23, 6), nullable=False)  # 成交额 （千元）



if __name__ == "__main__":
    pass