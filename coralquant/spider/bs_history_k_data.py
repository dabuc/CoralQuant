from datetime import datetime
import baostock as bs
import pandas as pd
import time

from tqdm import tqdm
from coralquant import logger
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.database import engine, session_scope, del_table_data
import concurrent.futures
from coralquant.stringhelper import frequency_odl_table_obj
from coralquant.settings import CQ_Config

_logger = logger.Logger(__name__).get_log()

d_fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
w_m_fields = 'date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg'
min_fields = 'date,time,code,open,high,low,close,volume,amount,adjustflag'

frequency_fields = {
    'd': d_fields,
    'w': w_m_fields,
    'm': w_m_fields,
    '5': min_fields,
    '15': min_fields,
    '30': min_fields,
    '60': min_fields
}


def _parse_data(content, ts_code, frequency, adjustflag):
    """
    解析数据，并保存
    """
    if content.empty:
        return

    table_name_key = get_table_name_key(adjustflag, frequency)

    table_name = frequency_odl_table_obj[table_name_key].__tablename__

    try:
        content['t_date'] = [datetime.strptime(x, '%Y-%m-%d').date() for x in content.date]
        content.to_sql(table_name, engine, schema=CQ_Config.DB_SCHEMA, if_exists='append', index=False)
    except Exception as e:  #traceback.format_exc(1)
        _logger.error('{}保存出错/{}'.format(ts_code, repr(e)))
    # else:
    #     _logger.info('{}保存成功'.format(ts_code))


def get_table_name_key(adjustflag, frequency):
    if adjustflag != '3':
        table_name_key = '{}-{}'.format(frequency, adjustflag)
    else:
        table_name_key = frequency
    return table_name_key


def _query_history_k_data_plus(fields: str, frequency: str, adjustflag: str) -> pd.DataFrame:
    """
    获取历史A股K线数据
    """
    
    table_name_key = get_table_name_key(adjustflag, frequency)

    try:
        taskEnum = TaskEnum(table_name_key)
    except Exception as e:
        _logger.error('获取历史A股K线数据/任务不存在，不能获取历史A股K线数据！')
        return
    #删除历史数据
    del_table_data(frequency_odl_table_obj[table_name_key])

    #### 登陆系统 ####
    lg = bs.login()

    step = 1
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as sm:
            rp = sm.query(TaskTable).filter(TaskTable.task == taskEnum.value, TaskTable.finished == False).all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                start_date = task.begin_date.strftime("%Y-%m-%d")
                end_date = task.end_date.strftime("%Y-%m-%d")

                max_try = 8  # 失败重连的最大次数

                for i in range(max_try):
                    rs = bs.query_history_k_data_plus(task.ts_code,
                                                      fields,
                                                      start_date=start_date,
                                                      end_date=end_date,
                                                      frequency=frequency,
                                                      adjustflag=adjustflag)
                    if rs.error_code == '0':
                        data_list = []
                        while (rs.error_code == '0') & rs.next():
                            # 获取一条记录，将记录合并在一起
                            data_list.append(rs.get_row_data())
                        #_logger.info('{}下载成功,数据{}条'.format(task.ts_code, len(data_list)))
                        result = pd.DataFrame(data_list, columns=rs.fields)
                        executor.submit(_parse_data, result, task.ts_code, frequency, adjustflag)
                        task.finished = True
                        step += 1
                        break
                    elif i < (max_try - 1):
                        time.sleep(2)
                        continue
                    else:
                        _logger.error('query_history_k_data_plus respond error_code:' + rs.error_code)
                        _logger.error('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

            sm.commit()
    #### 登出系统 ####
    bs.logout()


def init_history_k_data_plus(frequency, adjustflag="3"):
    """
    初始化历史K线数据
    """
    fields = frequency_fields[frequency]
    _query_history_k_data_plus(fields, frequency, adjustflag)
