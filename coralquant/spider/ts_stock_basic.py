# -*- coding: utf-8 -*-
"""股票列表"""
from coralquant.database import engine
from coralquant.settings import CQ_Config
from coralquant.models.odl_model import stock_basic
import tushare as ts
import pandas as pd
from sqlalchemy import delete


def convert_to_bscode(ts_code):
    """
    ts_code 转换成 bs_code
    """
    b=ts_code.split('.')
    bs_code = '{}.{}'.format(b[1].lower(),b[0])
    return bs_code


    

def get_stock_basic():
    """
    获取股票列表
    """

    pro = ts.pro_api(CQ_Config.TUSHARE_TOKEN)
    #查询当前所有正常上市交易的股票列表

    fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs'

    rs_L = pro.stock_basic(exchange='', list_status='L', fields=fields)
    rs_D = pro.stock_basic(exchange='', list_status='D', fields=fields)
    rs_P = pro.stock_basic(exchange='', list_status='P', fields=fields)

    result = pd.concat([rs_L, rs_D, rs_P])

    result['bs_code']=[convert_to_bscode(x) for x in result.ts_code]

    result.to_sql('odl_ts_stock_basic',
                engine,
                schema='stock_dw',
                if_exists='replace',
                index=False)


if __name__ == "__main__":
    pass
