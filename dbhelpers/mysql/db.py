import logging
from sqlalchemy import create_engine

import mysql.connector
from mysql.connector import MySQLConnection
from sqlalchemy import URL
import sqlalchemy


logger = logging.getLogger(__name__)

__DB: MySQLConnection = None


def get_db(
        **mysql_args       # can accept config, or dbpath...
) -> MySQLConnection:
    ''' returns new or existing connection'''
    global __DB
    
    logger.debug(f'{mysql_args = }')
    
    if __DB is None or not __DB.is_connected():
        __DB = mysql.connector.connect(**mysql_args )
    
    logger.debug(f'{__DB.connection_id = }')
    logger.debug(f'{__DB.database = }')
    return __DB


def get_engine(**mysql_args) -> sqlalchemy.Engine:
    logger.debug(f'{mysql_args = }')
    
    db_url = get_db_url(**mysql_args)
    engine = create_engine(
                db_url, 
                # paramstyle='qmark'
            )
    return engine


def test_connection() -> bool:
    ''' 
    tests the connection, returns True or False, logs error
    '''
    try:
        assert __DB.is_connected()
        return True
    except Exception as e:
        logger.critical(e)
        logger.critical('connection failed')
        return False


def get_db_url(
        user:str,
        password:str,
        host:str,
        database:str,
        driver:str="mysql+mysqlconnector"
) -> URL:

    logger.debug('creating db URL')
    url_object = URL.create(
        driver,
        username=user,
        password=password,  # plain (unescaped) text
        host=host,
        database=database,
    )
    return url_object


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s | %(funcName)s | %(message)s'
    )
    if test_connection():
        logger.info('Success connecting to db')
    else:
        logger.error('Failed connecting to db')