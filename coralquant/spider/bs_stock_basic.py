import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
from coralquant.settings import CQ_Config

engine = create_engine(CQ_Config.DATABASE_URL)
connection = engine.connect()


def get_stock_basic():
    """
    获取bs-A股股票列表
    """
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取证券基本资料
    rs = bs.query_stock_basic()
    # rs = bs.query_stock_basic(code_name="浦发银行")  # 支持模糊查询
    print('query_stock_basic respond error_code:'+rs.error_code)
    print('query_stock_basic respond  error_msg:'+rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 输出结果集
    result.to_sql('odl_bs_stock_basic',
                connection,
                schema='stock_dw',
                if_exists='replace',
                index=False)

    # 登出系统
    bs.logout()


if __name__ == "__main__":
    pass