from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd
import talib as ta
from coralquant.database import engine, session_scope
from coralquant.models import bdl_model
from coralquant.models.bdl_model import DailyKData2, DailyKTech
from coralquant.models.orm_model import TaskTable
from coralquant.stringhelper import TaskEnum
from coralquant.taskmanage import create_task
from sqlalchemy import and_, desc, select
from tqdm import tqdm


def save_data():
    """
    docstring
    """
    pass

def update_daily_tech_data(taskEnum:TaskEnum):
    """
    更新日线技术指标数据\n
    1.更新任务列表\n
    2.依据任务列表依次更新每个股票的技术指标数据
    """

    end_date=datetime.now().date()

    create_task(taskEnum,None,end_date=end_date,type=1,status=1,isdel=True)
    create_task(taskEnum,None,end_date=end_date,type=2,status=1,isdel=False)

    with ThreadPoolExecutor() as executor:
        with session_scope() as sm:
            rp = sm.query(TaskTable).filter(TaskTable.task == taskEnum.value, TaskTable.finished == False).all()

            for task in tqdm(rp):
                if task.finished:
                    continue

                table = bdl_model.Base.metadata.tables.get(DailyKData2.__tablename__)
                cols = [
                    table.c.id, table.c.date, table.c.code, table.c.open, table.c.high, table.c.low, table.c.close, table.c.preclose,
                    table.c.volume, table.c.amount, table.c.turn, table.c.pctChg
                ]

                # s = select([table.c.date]).where(table.c.code == task.ts_code).order_by(desc(table.c.date)).offset(249).limit(1)
                # r= engine.execute(s).first()
                # s = select(cols).where(and_(table.c.code == task.ts_code,table.c.date>=r.date)).order_by(table.c.date)

                s = select(cols).where(table.c.code == task.ts_code).order_by(table.c.date)

                df = pd.read_sql(s, engine)
                count= len(df)
                if count <1:
                    continue

                df['ma5'] = ta.SMA(df['close'], timeperiod=5)
                df['ma10'] = ta.SMA(df['close'], timeperiod=10)
                df['ma20'] = ta.SMA(df['close'], timeperiod=20)
                df['ma30'] = ta.SMA(df['close'], timeperiod=30)
                df['ma60'] = ta.SMA(df['close'], timeperiod=60)
                df['ma120'] = ta.SMA(df['close'], timeperiod=120)
                df['ma250'] = ta.SMA(df['close'], timeperiod=250)

                df['vol5'] = ta.SMA(df['volume'], timeperiod=5)
                df['vol10'] = ta.SMA(df['volume'], timeperiod=10)
                df['vol20'] = ta.SMA(df['volume'], timeperiod=20)
                df['vol60'] = ta.SMA(df['volume'], timeperiod=60)

                df['am']=(df['high']-df['low'])/df['preclose']
                df['am5']=ta.SMA(df['am'], timeperiod=5)
                df['am10']=ta.SMA(df['am'], timeperiod=10)
                df['am20']=ta.SMA(df['am'], timeperiod=20)
                df['am60']=ta.SMA(df['am'], timeperiod=60)
                
                df['wr3'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=3)
                df['wr5'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=5)
                df['wr10'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=10)
                df['wr20'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=20)
                df['wr60'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=60)
                df['wr120'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=120)
                df['wr250'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=250)
                df['wr888'] = ta.WILLR(df["high"],df["low"],df["close"], timeperiod=888)

                
                df.to_sql(DailyKTech.__tablename__, engine, schema='stock_dw', if_exists='append', index=False)



