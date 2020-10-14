from sqlalchemy import create_engine, select
from coralquant.settings import CQ_Config
engine = create_engine(CQ_Config.DATABASE_URL)