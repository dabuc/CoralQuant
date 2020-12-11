# -*- coding: utf-8 -*-
"""
操作数据层数据模型，用于保存原始数据
"""
from coralquant import logger
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, BigInteger, Numeric, String, Enum, Float, Boolean, Date, DateTime
from coralquant.database import Base, session_scope

_logger = logger.Logger(__name__).get_log()


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
    adjustflag = Column('adjustflag', String(1))  #复权状态(1：后复权， 2：前复权，3：不复权）
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


class D_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base, Base):
    """
    日线历史行情数据
    """
    __tablename__ = "odl_d_history_A_stock_k_data"


class W_History_A_Stock_K_Data(W_History_A_Stock_K_Data_Base, Base):
    """
    周线历史行情数据
    """
    __tablename__ = "odl_w_history_A_stock_k_data"


class M_History_A_Stock_K_Data(M_History_A_Stock_K_Data_Base, Base):
    """
    月线历史行情数据
    """
    __tablename__ = "odl_m_history_A_stock_k_data"


#-------前复权-A股K线数据----------


class D2_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base, Base):
    """
    前复权-日线历史行情数据
    """
    __tablename__ = "odl_d2_history_A_stock_k_data"


#------后复权------------
class D1_History_A_Stock_K_Data(D_History_A_Stock_K_Data_Base, Base):
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
    code = Column('code', String(10))  #证券代码
    pubDate = Column('pubDate', String(10))  #公司发布财报的日期
    statDate = Column('statDate', String(10))  #财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    roeAvg = Column('roeAvg', String(23))  #净资产收益率(平均)(%)
    npMargin = Column('npMargin', String(23))  #销售净利率(%)
    gpMargin = Column('gpMargin', String(23))  #销售毛利率(%)
    netProfit = Column('netProfit', String(23))  #净利润(元)
    epsTTM = Column('epsTTM', String(23))  #每股收益
    MBRevenue = Column('MBRevenue', String(23))  #主营营业收入(元)
    totalShare = Column('totalShare', String(23))  #总股本
    liqaShare = Column('liqaShare', String(23))  #流通股本


# =========================Tushare数据源模型============================


class TS_Stock_Basic(Base):
    """
    TS-证券基本资料
    """
    __tablename__ = "odl_ts_stock_basic"
    ts_code = Column("ts_code", String(10), primary_key=True)  # TS代码
    symbol = Column("symbol", String(6))  # 股票代码
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


class TS_Daily_Base:
    """
    日线行情数据
    """

    id = Column("id", Integer, primary_key=True)
    ts_code = Column("ts_code", String(10), nullable=False)  # 股票代码
    trade_date = Column("trade_date", Date, nullable=False)  # 交易日期
    open = Column("open", Numeric(12, 4), nullable=False)  # 开盘价
    high = Column("high", Numeric(12, 4), nullable=False)  # 最高价
    low = Column("low", Numeric(12, 4), nullable=False)  # 最低价
    close = Column("close", Numeric(12, 4), nullable=False)  # 收盘价
    pre_close = Column("pre_close", Numeric(12, 4))  # 昨收价
    change = Column("change", Numeric(12, 4))  # 涨跌额
    pct_chg = Column("pct_chg", Numeric(12, 4))  # 涨跌幅
    vol = Column("vol", Numeric(23, 4))  # 成交量 （手）
    amount = Column("amount", Numeric(23, 4))  # 成交额 （千元）


class TS_Daily(TS_Daily_Base, Base):
    """
    日线行情数据
    """
    __tablename__ = "odl_ts_daily"


class TS_Daily_hfq(TS_Daily_Base, Base):
    """
    后复权日线行情数据
    """
    __tablename__ = "odl_ts_daily_hfq"


class TS_Daily_Basic(Base):
    """
    每日指标
    """
    __tablename__ = "odl_ts_daily_basic"
    id = Column("id", Integer, primary_key=True)
    ts_code = Column("ts_code", String(10), nullable=False)  #TS股票代码
    trade_date = Column("trade_date", Date, nullable=False)  #交易日期
    close = Column("close", Numeric(18, 5))  #当日收盘价 7,4
    turnover_rate = Column("turnover_rate", Numeric(18, 5))  #换手率（%） 8,4
    turnover_rate_f = Column("turnover_rate_f", Numeric(18, 5))  #换手率（自由流通股）9,4
    volume_ratio = Column("volume_ratio", Numeric(18, 3))  #量比 8,2
    pe = Column("pe", Numeric(18, 5))  #市盈率（总市值/净利润， 亏损的PE为空）10,4
    pe_ttm = Column("pe_ttm", Numeric(18, 5))  #市盈率（TTM，亏损的PE为空）12,4
    pb = Column("pb", Numeric(18, 5))  #市净率（总市值/净资产）10,4
    ps = Column("ps", Numeric(18, 5))  #市销率 11,4
    ps_ttm = Column("ps_ttm", Numeric(18, 5))  #市销率（TTM）15,4
    dv_ratio = Column("dv_ratio", Numeric(18, 5))  #股息率 （%）7,4
    dv_ttm = Column("dv_ttm", Numeric(18, 5))  #股息率（TTM）（%）7,4
    total_share = Column("total_share", Numeric(18, 5))  #总股本 （万股）13,4
    float_share = Column("float_share", Numeric(18, 5))  #流通股本 （万股）13,4
    free_share = Column("free_share", Numeric(18, 5))  #自由流通股本 （万）12,4
    total_mv = Column("total_mv", Numeric(18, 5))  #总市值 （万元）14,4
    circ_mv = Column("circ_mv", Numeric(18, 5))  #流通市值（万元）14,4


class TS_TradeCal(Base):
    """
    交易日历
    """
    __tablename__ = "odl_ts_trade_cal"
    id = Column("id", Integer, primary_key=True)
    exchange = Column("exchange", String(10), nullable=False)  #交易所 SSE上交所 SZSE深交所
    cal_date = Column("cal_date", Integer, nullable=False)  #日历日期
    date = Column("date", Date, nullable=False)  #日历日期
    is_open = Column('is_open', Boolean, nullable=False)  #是否交易 0休市 1交易
    pretrade_date = Column("pretrade_date", Date)  #上一个交易日

    @staticmethod
    def del_all():
        """
        清空表数据
        """
        with session_scope() as sm:
            query = sm.query(TS_TradeCal).delete()
            sm.commit()
            _logger.info('交易日历表数据已清空')


class TS_Adj_Factor(Base):
    """
    复权因子
    """
    __tablename__ = "odl_ts_adj_factor"
    id = Column("id", Integer, primary_key=True)
    ts_code = Column("ts_code", String(10), nullable=False)
    trade_date = Column("trade_date", Date, nullable=False)
    adj_factor = Column("adj_factor", Float, nullable=False)


if __name__ == "__main__":
    pass