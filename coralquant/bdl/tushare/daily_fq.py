# -*- coding: utf-8 -*-
"""
计算日线行情复权数据
前复权	当日收盘价 × 当日复权因子 / 最新复权因子
后复权	当日收盘价 × 当日复权因子
"""
from typing import List
from coralquant.models.odl_model import TS_Adj_Factor, TS_Daily
from coralquant.database import session_scope
from coralquant.settings import CQ_Config
from sqlalchemy import and_, select, join
from coralquant.database import engine
import pandas as pd
from sqlalchemy.sql import func


def get_daily_qfq(codes: List):
    """
    获取前复权-日线行情数据
    """

    s_new_adj = select([TS_Adj_Factor.ts_code,
                        func.max(TS_Adj_Factor.trade_date).label('m_date')
                        ]).where(TS_Adj_Factor.ts_code.in_(codes)).group_by(TS_Adj_Factor.ts_code).cte('s_new_adj')

    j = join(TS_Adj_Factor, s_new_adj,
             and_(TS_Adj_Factor.trade_date == s_new_adj.c.m_date, TS_Adj_Factor.ts_code == s_new_adj.c.ts_code))
    statement = select([
        TS_Adj_Factor.ts_code,
        TS_Adj_Factor.trade_date.label('new_date'),
        TS_Adj_Factor.adj_factor.label('new_adj_factor')
    ]).select_from(j)

    new_adj_df = pd.read_sql(statement, engine)  #获取最新的复权因子

    cols = [
        TS_Daily.id, TS_Daily.ts_code, TS_Daily.trade_date, TS_Daily.open, TS_Daily.high, TS_Daily.low, TS_Daily.close,
        TS_Daily.pre_close, TS_Daily.change, TS_Daily.pct_chg, TS_Daily.vol, TS_Daily.amount, TS_Adj_Factor.adj_factor
    ]

    j = join(TS_Daily,
             TS_Adj_Factor,
             and_(TS_Daily.trade_date == TS_Adj_Factor.trade_date, TS_Daily.ts_code == TS_Adj_Factor.ts_code),
             isouter=True)

    s = select(cols).select_from(j).where(TS_Daily.ts_code.in_(codes))
    df = pd.read_sql(s, engine)
    df = pd.merge(df, new_adj_df, on='ts_code', how='left')
    df = df.sort_values(by=['ts_code', 'trade_date'])
    # df['open']  = df['open'] * df['adj_factor']/df['new_adj_factor']
    # df['high']  = df['high'] * df['adj_factor']/df['new_adj_factor']
    # df['low']  = df['low'] * df['adj_factor']/df['new_adj_factor']
    # df['close']  = df['close'] * df['adj_factor']/df['new_adj_factor']
    df['p_close'] = df.groupby('ts_code')['close'].shift(1)
    df.to_csv('test.csv', index=False)

    print(df)


def update_daily_hfq():
    """
    更新后复权数据
    """
    
    pass