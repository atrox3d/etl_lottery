import logging
import pandas as pd

# https://docs.sqlalchemy.org/en/20/core/engines.html
from sqlalchemy import create_engine
from sqlalchemy import URL
# 
# engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")

logger = logging.getLogger(__name__)

def get_db_url(
        user:str,
        password:str,
        host:str,
        database:str,
        driver:str="mysql+mysqlconnector"
) -> URL:

    logger.info('creating db URL')
    url_object = URL.create(
        driver,
        username=user,
        password=password,  # plain (unescaped) text
        host=host,
        database=database,
    )
    return url_object


def load_to_mysql(df:pd.DataFrame, url_object:URL):

    logger.info('creating engine')
    logger.info(f'driver    : {url_object.drivername}')
    logger.info(f'host      : {url_object.host}')
    logger.info(f'user      : {url_object.username}')
    logger.info(f'password  : {url_object.password}')
    logger.info(f'databse   : {url_object.database}')
    engine = create_engine(url_object)
    
    logger.info('loading to mysql')
    df.to_sql(name='lotteria', con=engine, if_exists='replace', index=True)
    
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

