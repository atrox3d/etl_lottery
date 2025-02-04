import logging

import mysql.connector
from mysql.connector import MySQLConnection
from sqlalchemy import URL
from .config import build_config, load_config, get_default_config

logger = logging.getLogger(__name__)

__DB: MySQLConnection = None


def get_db(config:dict=get_default_config()) -> MySQLConnection:
    ''' returns new connection'''
    global __DB
    
    logger.debug(f'{config = }')
    
    if __DB is None or not __DB.is_connected():
        __DB = mysql.connector.connect(**config )
    
    logger.debug(f'{__DB.connection_id = }')
    logger.debug(f'{__DB.database = }')
    return __DB


def test_connection(config:dict|None=None) -> bool:
    ''' 
    tests the connection
    returns user, host, port
    '''
    try:
        db = get_db(config or get_default_config())
        assert db.is_connected()
        
        db.close()
        assert not db.is_connected()
        return True
    except:
        logger.critical('connection failed')
        return False


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


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s | %(funcName)s | %(message)s'
    )
    if test_connection():
        logger.info('Success connecting to db')
    else:
        logger.error('Failed connecting to db')