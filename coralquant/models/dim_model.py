from sqlalchemy.sql.schema import Index
from coralquant import logger
from datetime import date
from coralquant.database import Base, session_maker
from sqlalchemy import Integer, Column, Date, SmallInteger, String
import datetime as dt

_logger = logger.Logger(__name__).get_log()


class DIM_Date(Base):
    """
    日期维度表
    """
    __tablename__ = "dim_date"
    idate = Column(Integer, nullable=False, primary_key=True)  #年月日
    date = Column(Date, nullable=False, unique=True, index=True)  #年月日
    year_month = Column(Integer, nullable=False)  #年月
    year = Column(Integer, nullable=False)  #年
    weekNum = Column(String(7), nullable=False)  #所属年份的第几周
    week = Column(SmallInteger, nullable=False)
    __table_args__ = (Index('IDX_DATE_YEAR_MONTH', date, year_month), Index('IDX_DATE_WEEKNUM', date, weekNum))

    @staticmethod
    def init_data():
        """
        初始化日期维度表数据
        """
        begin_date = dt.datetime.strptime('1990-12-01', '%Y-%m-%d')
        end_date = dt.datetime.strptime('2025-12-31', '%Y-%m-%d')
        date_list: list[date] = []
        while begin_date <= end_date:
            date_list.append(begin_date)
            begin_date += dt.timedelta(1)

        with session_maker() as sn:
            for tmpdate in date_list:
                row = DIM_Date(idate=tmpdate.year * 10000 + tmpdate.month * 100 + tmpdate.day,
                               date=tmpdate,
                               year_month=tmpdate.year * 100 + tmpdate.month,
                               year=tmpdate.year,
                               weekNum='{}-{}'.format(tmpdate.year, tmpdate.strftime('%W')),
                               week=tmpdate.weekday())

                sn.add(row)

        _logger.info('日期维度表初始化完成')
