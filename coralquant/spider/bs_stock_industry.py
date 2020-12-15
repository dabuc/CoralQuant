import baostock as bs
import pandas as pd
from coralquant.database import engine
from sqlalchemy import String
from coralquant.settings import CQ_Config

def create_stock_industry():
    """
    BS-创建行业分类
    """
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取行业分类数据
    rs = bs.query_stock_industry()
    print('query_stock_industry error_code:' + rs.error_code)
    print('query_stock_industry respond  error_msg:' + rs.error_msg)

    # 打印结果集
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)

    dtype = {
        'updateDate': String(10),
        'code': String(9),
        'code_name': String(10),
        'industry': String(4),
        'industryClassification': String(6)
    }

    result.to_sql('odl_bs_stock_industry', engine, schema=CQ_Config.DB_SCHEMA, if_exists='replace', index=False, dtype=dtype)

    # 登出系统
    bs.logout()
