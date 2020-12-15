from coralquant.util.dataconvert import convert_to_date, convert_to_tscode, get_int_from_str
from coralquant.models.odl_model import BS_Stock_Basic
from datetime import datetime
import baostock as bs
import pandas as pd
from coralquant.database import engine
from coralquant.settings import CQ_Config

def get_stock_basic():
    """
    获取最新BS-A股股票列表
    """
    #清空原有数据
    BS_Stock_Basic.del_all_date()

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
    result['updated_on']=datetime.now()

    result['status'] = [None if x == "" else bool(get_int_from_str(x)) for x in result["status"]]
    result['ipoDate'] = [convert_to_date(x, '%Y-%m-%d') for x in result.ipoDate]
    result['outDate'] = [convert_to_date(x, '%Y-%m-%d') for x in result.outDate]
    result['ts_code'] = [convert_to_tscode(x) for x in result.code]


    


    # 输出结果集
    result.to_sql('odl_bs_stock_basic',
                engine,
                schema=CQ_Config.DB_SCHEMA,
                if_exists='append',
                index=False)

    # 登出系统
    bs.logout()


if __name__ == "__main__":
    pass