import concurrent.futures
from coralquant.models.odl_model import Profit_Data
from coralquant.models.bdl_model import quarterly_Profit_Data
from datetime import datetime

from coralquant import logger
from coralquant.database import session_scope
from sqlalchemy.sql import func
from coralquant.util import dataconvert as dc

_logger = logger.Logger(__name__).get_log()

def _build_result_data(rp):
    """
    构建结果数据列表
    """
    result = []
    for row in rp:
        tmp = {
            'code': row.code,
            'pubDate': datetime.strptime(row.pubDate, "%Y-%m-%d").date(),
            'statDate': datetime.strptime(row.statDate, "%Y-%m-%d").date(),
            'roeAvg': dc.get_decimal_from_str(row.roeAvg),
            'npMargin': dc.get_decimal_from_str(row.npMargin),
            'gpMargin': dc.get_decimal_from_str(row.gpMargin),
            'netProfit': dc.get_decimal_from_str(row.netProfit),
            'epsTTM': dc.get_decimal_from_str(row.epsTTM),
            'MBRevenue': dc.get_decimal_from_str(row.MBRevenue),
            'totalShare': dc.get_decimal_from_str(row.totalShare),
            'liqaShare': dc.get_decimal_from_str(row.liqaShare),
        }
        result.append(tmp)
    return result

def _build_to_table(dic):
    to_table = quarterly_Profit_Data()
    to_table.code = dic['code']
    to_table.pubDate = dic['pubDate']
    to_table.statDate = dic['statDate']
    to_table.roeAvg = dic['roeAvg']
    to_table.npMargin = dic['npMargin']
    to_table.gpMargin = dic['gpMargin']
    to_table.netProfit = dic['netProfit']
    to_table.epsTTM = dic['epsTTM']
    to_table.MBRevenue = dic['MBRevenue']
    to_table.totalShare = dic['totalShare']
    to_table.liqaShare = dic['liqaShare']
    return to_table

def _insert_data(data: list, pagenum):
    """
    导入数据
    """
    ins_data = []
    num = 0  #计数
    try:
        with session_scope() as session:
            for dic in data:
                to_table = _build_to_table(dic)
                ins_data.append(to_table)
                num += 1
                dm = divmod(num, 1000)
                if dm[1] == 0:
                    session.bulk_save_objects(ins_data)
                    session.commit()
                    ins_data.clear()
            if len(ins_data) > 0:
                session.bulk_save_objects(ins_data)
                session.commit()
    except Exception as e:
        _logger.error("第{}页数据导入失败:{}".format(pagenum, repr(e)))
    else:
        _logger.info("第{}页数据导入完成".format(pagenum))


def import_data():
    """
    导入日线数据
    """
    #offset：当偏移量大于800万时，offset limit模式性能下降严重，查询一次要12秒……
    #改成直接定位主键id查询。

    from_table = Profit_Data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as session:
            onerow = session.query(func.min(from_table.id), func.max(from_table.id)).one()
            minid = onerow[0]
            maxid = onerow[1]

            if not minid:  #没有数据
                return

            pagesize = 5000
            ahead_id = minid
            next_id = ahead_id + pagesize
            i = 0  #计数
            while True:
                if ahead_id > maxid:
                    break
                rp = session.query(from_table).filter(from_table.id >= ahead_id, from_table.id < next_id)
                to_data = _build_result_data(rp)
                executor.submit(_insert_data, to_data, i + 1)
                i += 1
                ahead_id = next_id
                next_id = ahead_id + pagesize
    
    _logger.info("数据导入完成")


if __name__ == "__main__":
    pass
