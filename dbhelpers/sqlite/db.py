import logging
import sqlite3
from sqlalchemy import create_engine
import sqlalchemy

# import mysql.connector
# from mysql.connector import MySQLConnection
# from sqlalchemy import URL
# from .config import get_default_config

logger = logging.getLogger(__name__)

__DB: sqlite3.Connection = None


def get_db(
        **conn_args       # can accept config, or dbpath...
) -> sqlite3.Connection:
    ''' returns new or existing connection'''
    global __DB
    
    logger.debug(f'{conn_args = }')
    dbpath = conn_args.get('dbpath')
    logger.debug(f'{dbpath = }')
    if not dbpath:
        raise ValueError('dbpath is required')
    logger.debug(f'{dbpath = }')
    
    if __DB is None:
        __DB = sqlite3.connect(dbpath )
    
    return __DB


def get_engine(**conn_args) -> sqlalchemy.Engine:
    logger.debug(f'{conn_args = }')
    dbpath = conn_args.get('dbpath')
        
    logger.debug(f'{dbpath = }')
    if not dbpath:
        raise ValueError('dbpath is required')
    logger.debug(f'{dbpath = }')

    db_url = get_db_url(dbpath=dbpath)
    engine = create_engine(db_url)
    
    return engine


def test_connection(**conn_args) -> bool:
    ''' 
    tests the connection, returns True or False, logs error
    '''
    try:
        logger.debug(f'{conn_args = }')
        dbpath = conn_args.get('dbpath')
        
        logger.debug(f'{dbpath = }')
        if not dbpath:
            raise ValueError('dbpath is required')
        logger.debug(f'{dbpath = }')
        db = get_db(dbpath=dbpath)
        return True
    except Exception as e:
        logger.critical('connection failed')
        logger.critical(e)
        return False


def get_db_url(**conn_args) -> str:
    logger.debug(f'{conn_args = }')
    dbpath = conn_args.get('dbpath')
    
    logger.debug(f'{dbpath = }')
    if not dbpath:
        raise ValueError('dbpath is required')
    logger.debug(f'{dbpath = }')
    logger.info('creating db URL')
    url = f'sqlite:///{dbpath}'
    return url


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s | %(funcName)s | %(message)s'
    )
    if test_connection(dbpath='testing.db'):
        logger.info('Success connecting to db')
    else:
        logger.error('Failed connecting to db')