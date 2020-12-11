from coralquant import logger
from datetime import datetime
from coralquant.settings import CQ_Config
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
import concurrent.futures
from coralquant.database import get_new_session
from tqdm import tqdm
import time

_logger = logger.Logger(__name__).get_log()


def extract_data(taskEnum: TaskEnum, pro_api_func, pro_api_func_pramas: dict, load_data_func,
                 load_data_func_params: dict, log_desc: str):
    """
    抽取远端数据
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        sm = get_new_session()
        try:
            rp = sm.query(TaskTable).filter(TaskTable.task == taskEnum.value, TaskTable.finished == False)
            if CQ_Config.IDB_DEBUG == '1':  #如果是测试环境
                rp = rp.limit(10)

            rp = rp.all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                max_try = 8  # 失败重连的最大次数
                for i in range(max_try):
                    try:
                        tasktime = datetime.strftime(task.begin_date, '%Y%m%d')
                        pro_api_func_pramas['trade_date'] = tasktime
                        result = pro_api_func(**pro_api_func_pramas)

                        load_data_func_params['result'] = result
                        load_data_func_params['task_date'] = task.begin_date
                        executor.submit(load_data_func, load_data_func_params)

                        task.finished = True
                        time.sleep(0.2)
                        break
                    except Exception as e:
                        if i < (max_try - 1):
                            t = (i + 1) * 2
                            time.sleep(t)
                            logger.error('[{}]异常重连/{}'.format(task.ts_code, repr(e)))
                            continue
                        else:
                            _logger.error('获取[{}]{}失败/{}'.format(task.ts_code, log_desc, repr(e)))
                            raise
            sm.commit()
        except:
            pass
        finally:
            pass
