# -*- coding: utf-8 -*-
"""
基础数据层数据模型
"""
from datetime import datetime

from coralquant.database import Base
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, MetaData,
                        Numeric, String, UniqueConstraint)
from sqlalchemy.orm import relationship


class DailyKDataBase():
    """
    日线数据基类
    """
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
    float_share= Column('float_share', Numeric(23, 6), nullable=False)  #流通股本 （万股）
    tradestatus = Column('tradestatus', Boolean, nullable=False)  #交易状态
    pctChg = Column('pctChg', Float, nullable=False)  #涨跌幅（百分比）
    peTTM = Column('peTTM', Float, nullable=False)  #滚动市盈率
    pbMRQ = Column('pbMRQ', Float, nullable=False)  #滚动市销率
    psTTM = Column('psTTM', Float, nullable=False)  #滚动市现率
    pcfNcfTTM = Column('pcfNcfTTM', Float, nullable=False)  #市净率
    isST = Column('isST', Boolean, nullable=False)  #是否ST


class WeeklyKDataBase():
    """
    周线数据基类
    """
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


class MonthlyKDataBase():
    """
    月线数据
    """
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


#-------不复权-----------


class DailyKData(DailyKDataBase, Base):
    """
    日线数据
    """
    __tablename__ = "bdl_bs_daily_k_data"


class WeeklyKData(WeeklyKDataBase, Base):
    """
    周线数据
    """
    __tablename__ = "bdl_bs_weekly_k_data"


class MonthlyKData(MonthlyKDataBase, Base):
    """
    月线数据
    """
    __tablename__ = "bdl_bs_monthly_k_data"


#-------前复权-----------


class DailyKData2(DailyKDataBase, Base):
    """
    日线数据
    """
    __tablename__ = "bdl_bs_daily_2k_data"


class WeeklyKData2(WeeklyKDataBase, Base):
    """
    周线数据
    """
    __tablename__ = "bdl_bs_weekly_2k_data"


class MonthlyKData2(MonthlyKDataBase, Base):
    """
    月线数据
    """
    __tablename__ = "bdl_bs_monthly_2k_data"


#---------后复权--------------
class DailyKData1(DailyKDataBase, Base):
    """
    日线数据
    """
    __tablename__ = "bdl_bs_daily_1k_data"


#------财务数据----------------


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


#---------技术指标--------------
class DailyK2Tech():
    """
    前复权日线数据-技术分析指标表
    """
    pass

class DailyKTech(Base):
    """
    日线数据-技术分析指标表
    """
    __tablename__ = "bdl_bs_daily_k_tech"
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
    turn = Column('turn', Float, nullable=False)  #换手率
    pctChg = Column('pctChg', Float, nullable=False)  #涨跌幅（百分比）

    ma5 = Column('ma5', Numeric(12, 4))  #5日移动均价
    ma10 = Column('ma10', Numeric(12, 4))  #10日移动均价
    ma20 = Column('ma20', Numeric(12, 4))  #20日移动均价
    ma30 = Column('ma30', Numeric(12, 4))  #30日移动均价
    ma60 = Column('ma60', Numeric(12, 4))  #60日移动均价
    ma120 = Column('ma120', Numeric(12, 4))  #120日移动均价
    ma250 = Column('ma250', Numeric(12, 4))  #250日移动均价

    vol5 = Column('vol5', Numeric(23, 4))  #5日成交量均值
    vol10 = Column('vol10', Numeric(23, 4))  #10日成交量均值
    vol20 = Column('vol20', Numeric(23, 4))  #20日成交量均值
    vol60 = Column('vol60', Numeric(23, 4))  #60日成交量均值

    am  = Column('am', Numeric(12, 4))  #振幅
    am5  = Column('am5', Numeric(12, 4))  #5日振幅均值
    am10  = Column('am10', Numeric(12, 4))  #10日振幅均值
    am20  = Column('am20', Numeric(12, 4))  #20日振幅均值
    am60  = Column('am60', Numeric(12, 4))  #60日振幅均值

    hph = Column('hph', Numeric(12, 4))  #历史最高价
    lph = Column('lph', Numeric(12, 4))  #历史最低价
    
    wr3 = Column('wr3', Numeric(12, 4))#威廉3日指数
    wr5 = Column('wr5', Numeric(12, 4))#威廉5日指数
    wr10 = Column('wr10', Numeric(12, 4))#威廉10日指数
    wr20 = Column('wr20', Numeric(12, 4))#威廉20日指数
    wr60 = Column('wr60', Numeric(12, 4))#威廉60日指数
    wr120 = Column('wr120', Numeric(12, 4))#威廉120日指数
    wr250 = Column('wr250', Numeric(12, 4))#威廉250日指数
    wr888 = Column('wr888', Numeric(12, 4))#威廉888日指数
    

class BS_LaterNPctChg(Base):
    """
    docstring
    """
    __tablename__ = "bdl_bs_ln_pctchg"
    id = Column('id', Integer, primary_key=True)
    code = Column('code', String(10), nullable=False)  #BS证券代码 格式：sh.600000。sh：上海，sz：深圳
    date = Column('date', Date, nullable=False)  #交易所行情日期
    close = Column('close', Numeric(18, 4), nullable=False)  #今收盘价 精度：小数点后4位；单位：人民币元
    pctChg = Column('pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l5_pctChg = Column('l5_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l10_pctChg = Column('l10_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l20_pctChg = Column('l20_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l60_pctChg = Column('l60_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l120_pctChg = Column('l120_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    l250_pctChg = Column('l250_pctChg', Numeric(18, 6))  #涨跌幅（百分比）	精度：小数点后6位
    #daily_hfq_id = Column('id', Integer, ForeignKey('odl_bs_daily_hfq.id')) #关联BS_Daily_hfq的外键

    __table_args__ = (UniqueConstraint('code', 'date', name='UDX_CODE_DATE'), )
    


if __name__ == "__main__":
    pass
