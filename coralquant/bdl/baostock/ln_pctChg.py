"""
计算指定日期往后的5日，10日，20日，60日，120日，250日涨跌幅
"""

import datetime
from datetime import datetime as dtime

from pandas.core.frame import DataFrame

from coralquant import logger
from coralquant.database import session_scope, engine
from coralquant.models.bdl_model import BS_LaterNPctChg
from coralquant.models.odl_model import BS_Daily_hfq
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.util.dataconvert import convert_to_tscode
from sqlalchemy import and_, func, select, Table, desc, MetaData, Index, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from coralquant.database import engine
import pandas as pd
import numpy as np
from tqdm import tqdm
import concurrent.futures
from coralquant.settings import CQ_Config

_logger = logger.Logger(__name__).get_log()


def _calc_n_pctChg(df, n: int):
    """
    计算往后N日涨跌幅
    """
    ln_pctChg = "l{}_pctChg".format(n)
    tmp = df["close"].shift(n)
    df[ln_pctChg] = (tmp - df["close"]) * 100 / df["close"]  # .round(6)


def calc_later_n_pctChg():
    """
    计算股票后期的1日，2日，3日，5日，8日，10日，13日，20日，30日，60日，120日，250日涨跌幅
    1、先插入新增数据
    2、更新后期N日涨跌幅
    """
    _insert_new_data()
    _update_to_tmp_table("tmp_bs_laternpctchg")

    metadata = MetaData()
    bdl_bs_ln_pctchg = Table("bdl_bs_ln_pctchg", metadata, autoload=True, autoload_with=engine)
    tmp_bs_ln_pctchg = Table("tmp_bs_laternpctchg", metadata, autoload=True, autoload_with=engine)
    tmp_index = Index("idx_code_date", tmp_bs_ln_pctchg.c.code, tmp_bs_ln_pctchg.c.date)
    tmp_index.create(bind=engine)

    u = (
        bdl_bs_ln_pctchg.update()
        .values(
            l1_pctChg=tmp_bs_ln_pctchg.c.l1_pctChg,
            l2_pctChg=tmp_bs_ln_pctchg.c.l2_pctChg,
            l3_pctChg=tmp_bs_ln_pctchg.c.l3_pctChg,
            l5_pctChg=tmp_bs_ln_pctchg.c.l5_pctChg,
            l8_pctChg=tmp_bs_ln_pctchg.c.l8_pctChg,
            l10_pctChg=tmp_bs_ln_pctchg.c.l10_pctChg,
            l13_pctChg=tmp_bs_ln_pctchg.c.l13_pctChg,
            l20_pctChg=tmp_bs_ln_pctchg.c.l20_pctChg,
            l30_pctChg=tmp_bs_ln_pctchg.c.l30_pctChg,
            l60_pctChg=tmp_bs_ln_pctchg.c.l60_pctChg,
            l120_pctChg=tmp_bs_ln_pctchg.c.l120_pctChg,
            l250_pctChg=tmp_bs_ln_pctchg.c.l250_pctChg,
        )
        .where(
            and_(
                bdl_bs_ln_pctchg.c.code == tmp_bs_ln_pctchg.c.code, bdl_bs_ln_pctchg.c.date == tmp_bs_ln_pctchg.c.date
            )
        )
    )

    engine.execute(u)
    tmp_bs_ln_pctchg.drop(engine)
    _logger.info("更新数据完成，临时表已删除")


def _update_to_tmp_table(tmp_table_name: str):
    """创建更新数据到临时表"""
    _logger.info("创建更新数据到临时表")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with session_scope() as sm:
            # 获取所有需要更新的数据
            query = sm.query(BS_LaterNPctChg.code, func.min(BS_LaterNPctChg.date).label("mi_date"))
            query = query.filter(BS_LaterNPctChg.l250_pctChg == None)  # noqa
            query = query.group_by(BS_LaterNPctChg.code)
            rp = query.all()
            for row in tqdm(rp):
                s = (
                    select(
                        [
                            BS_Daily_hfq.id,
                            BS_Daily_hfq.code,
                            BS_Daily_hfq.date,
                            BS_Daily_hfq.close,
                            BS_Daily_hfq.pctChg,
                        ]
                    )
                    .where(and_(BS_Daily_hfq.code == row.code, BS_Daily_hfq.date >= row.mi_date))
                    .order_by(desc(BS_Daily_hfq.date))
                )
                df = pd.read_sql(s, engine)
                # 1日，2日，3日，5日，8日，10日，13日，20日，30日，60日，120日，250日
                _calc_n_pctChg(df, 1)
                _calc_n_pctChg(df, 2)
                _calc_n_pctChg(df, 3)
                _calc_n_pctChg(df, 5)
                _calc_n_pctChg(df, 8)
                _calc_n_pctChg(df, 10)
                _calc_n_pctChg(df, 13)
                _calc_n_pctChg(df, 20)
                _calc_n_pctChg(df, 30)
                _calc_n_pctChg(df, 60)
                _calc_n_pctChg(df, 120)
                _calc_n_pctChg(df, 250)
                df = df.replace([np.inf, -np.inf], np.nan)
                executor.submit(_save_tmp_data, df, tmp_table_name)


def _insert_new_data():
    """插入新增的记录"""
    # 获取所有需要插入的数据
    s = (
        "insert into bdl_bs_ln_pctchg(id,code,date,close,pctChg) "
        "select a.id,a.code,a.date,a.close,a.pctChg "
        "from odl_bs_daily_hfq a left join bdl_bs_ln_pctchg b on a.code = b.code and a.date =b.date "
        "where b.code is null"
    )
    engine.execute(s)


def _save_tmp_data(df: DataFrame, tmp_table_name: str):
    """
    更新 BS_LaterNPctChg 数据表
    """
    dtype = {"code": String(10)}
    df.to_sql(tmp_table_name, engine, schema=CQ_Config.DB_SCHEMA, if_exists="append", index=False, dtype=dtype)


def _set_pctChg(pctChg):
    if pd.isnull(pctChg):
        return None
    else:
        return pctChg
