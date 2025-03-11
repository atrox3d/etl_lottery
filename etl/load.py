import logging
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy import URL, exc
from sqlalchemy.exc import DatabaseError

# 
# engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")

logger = logging.getLogger(__name__)


def create_mysql_db(
        url_object  :URL,
        db_name     :str
):
    '''create db if not exists, useful when recreating docker service'''
    
    logger.info('creating engine')
    engine = create_engine(url_object)
    
    try:
        with engine.begin() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            logger.info("Database 'testing' created successfully")
    except exc.OperationalError as e:
        logger.error(f"Failed to create database: {e}")
        raise
    except exc.SQLAlchemyError as e:
        logger.error(f"Failed to create database: {e}")
        raise
    
    
def load_to_mysql(
        df          :pd.DataFrame, 
        url_object  :URL,
        replace     :bool = True,
        index       :bool = True
):
    '''loadf df to mysql'''
    
    logger.info('creating engine')
    logger.info(f'driver    : {url_object.drivername}')
    logger.info(f'host      : {url_object.host}')
    logger.info(f'user      : {url_object.username}')
    logger.info(f'password  : {url_object.password}')
    logger.info(f'database  : {url_object.database}')
    
    replace = 'replace' if replace else 'fail'
    logger.info(f'replace   : {replace}')
    logger.info(f'index     : {index}')
    
    engine = create_engine(url_object)
    
    logger.info('loading to mysql')
    df.to_sql(
        name='lotteria', 
        con=engine, 
        if_exists=replace, 
        index=index
    )


def load_to_sqlite(
        df          :pd.DataFrame, 
        url         :str,
        replace     :bool = True,
        index       :bool = True
):
    '''loadf df to sqlite'''
    
    logger.info('creating engine')
    logger.info(f'database  : {url}')
    
    replace = 'replace' if replace else 'fail'
    logger.info(f'replace   : {replace}')
    logger.info(f'index     : {index}')
    
    engine = create_engine(url)
    
    logger.info('loading to sqlite')
    df.to_sql(
        name='lotteria', 
        con=engine, 
        if_exists=replace, 
        index=index
    )
    
# conn = engine.connect()
# print(conn.closed)


# default
# engine = create_engine("mysql://scott:tiger@localhost/foo")

# mysqlclient (a maintained fork of MySQL-Python)
# engine = create_engine("mysql+mysqldb://scott:tiger@localhost/foo")

# PyMySQL
# engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")

# The MySQL Connector/Python DBAPI has had many issues since its release, some of which may remain unresolved, 
# and the mysqlconnector dialect is not tested as part of SQLAlchemy’s continuous integration. 
# The recommended MySQL dialects are mysqlclient and PyMySQL.
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

