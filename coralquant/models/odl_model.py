# -*- coding: utf-8 -*-
"""
操作数据层数据模型，用于保存原始数据
"""
from sqlalchemy import MetaData, Table, Column, Integer, BigInteger, Numeric, String, Enum, Float, Boolean, Date
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


if __name__ == "__main__":
    pass