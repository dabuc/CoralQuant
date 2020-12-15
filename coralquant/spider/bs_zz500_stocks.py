import baostock as bs
import pandas as pd
from sqlalchemy import String
from coralquant.database import engine
from coralquant.settings import CQ_Config

def get_zz500_stocks():
    """
    获取中证500成分股
    """

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取中证500成分股
    rs = bs.query_zz500_stocks()
    print('query_zz500 error_code:'+rs.error_code)
    print('query_zz500  error_msg:'+rs.error_msg)

    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)

    dtype = {'updateDate': String(10), 'code': String(9), 'code_name': String(10)}

    result.to_sql('odl_bs_zz500_stocks', engine, schema=CQ_Config.DB_SCHEMA, if_exists='replace', index=False, dtype=dtype)

    # 登出系统
    bs.logout()




if __name__ == "__main__":
    pass