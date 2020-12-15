import baostock as bs
import pandas as pd
from sqlalchemy import String
from coralquant.database import engine
from coralquant.settings import CQ_Config

def get_hs300_stocks():
    """
    获取沪深300成分股
    """

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取沪深300成分股
    rs = bs.query_hs300_stocks()
    print('query_hs300 error_code:' + rs.error_code)
    print('query_hs300  error_msg:' + rs.error_msg)

    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
    # # 结果集输出到csv文件
    # result.to_csv("hs300_stocks.csv", encoding="utf-8", index=False)

    dtype = {'updateDate': String(10), 'code': String(9), 'code_name': String(10)}

    result.to_sql('odl_bs_hs300_stocks', engine, schema=CQ_Config.DB_SCHEMA, if_exists='replace', index=False, dtype=dtype)

    # 登出系统
    bs.logout()