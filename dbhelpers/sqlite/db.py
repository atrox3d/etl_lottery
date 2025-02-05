import logging
import sqlite3
from sqlalchemy import create_engine
import sqlalchemy






logger = logging.getLogger(__name__)

__DB: sqlite3.Connection = None


def get_db(
        sqlitepath:str
) -> sqlite3.Connection:
    ''' returns new or existing connection'''
    global __DB
    
    logger.debug(f'{sqlitepath = }')

    if __DB is None:
        __DB = sqlite3.connect(sqlitepath)
    
    __DB.cursor().close()
    
    return __DB


def get_engine(sqlitepath:str) -> sqlalchemy.Engine:
    logger.debug(f'{sqlitepath = }')
    
    db_url = get_db_url(sqlitepath)
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
        __DB.cursor().close()
        return True
    except Exception as e:
        logger.critical(e)
        logger.critical('connection failed')
        return False


def get_db_url(sqlitepath:str) -> str:
    logger.debug(f'{sqlitepath = }')
    logger.info('creating db URL')
    url = f'sqlite:///{sqlitepath}'
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
