from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from coralquant.settings import CQ_Config

engine = create_engine(CQ_Config.DATABASE_URL)

Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


@contextmanager
def session_maker(session=session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
