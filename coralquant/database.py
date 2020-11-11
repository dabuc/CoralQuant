from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from coralquant.settings import CQ_Config

engine = create_engine(CQ_Config.DATABASE_URL)

Session = sessionmaker(bind=engine)
Base = declarative_base()
session=Session()

def get_new_session():
    """
    获取新Session
    """
    session=Session()
    return session

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


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



def del_table_data(table:Base):
    """
    清空指定表
    """
    with session_scope() as sn:
        sn.query(table).delete()