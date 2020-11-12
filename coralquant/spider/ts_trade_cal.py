"""TS-交易日历"""
import tushare as ts
import pandas as pd
from coralquant.database import engine
from coralquant.settings import CQ_Config
from sqlalchemy import Boolean, String, Integer, Date
from datetime import datetime


def create_cal_date():
    """
    创建交易日历
    """
    pro = ts.pro_api(CQ_Config.TUSHARE_TOKEN)
    df_SSE = pro.trade_cal(exchange='SSE')
    df_SZSE = pro.trade_cal(exchange='SZSE')
    result = pd.concat([df_SSE, df_SZSE])

    result['date'] = [datetime.strptime(x, '%Y%m%d').date() for x in result.cal_date]

    result['cal_date'] = [int(x) for x in result.cal_date]



    dtype = {'exchange': String(4), 'cal_date': Integer(), 'is_open': Boolean(), 'date': Date}

    result.to_sql('odl_ts_trade_cal', engine, schema='stock_dw', if_exists='replace', index=False, dtype=dtype)
