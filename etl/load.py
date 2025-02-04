import logging
import pandas as pd

# https://docs.sqlalchemy.org/en/20/core/engines.html
from sqlalchemy import create_engine
from sqlalchemy import URL
# 
# engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")

logger = logging.getLogger(__name__)

def load_to_mysql(
        df          :pd.DataFrame, 
        url_object  :URL,
        replace     :bool = True,
        index       :bool = True
):

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

