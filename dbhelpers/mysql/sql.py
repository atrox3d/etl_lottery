import logging
from dbhelpers.mysql.db import get_db
from mysql.connector import MySQLConnection

logger = logging.getLogger(__name__)

def exec_statement(
    stmt:str, *args,
    db:MySQLConnection=None,
    commit:bool=False,
    # close:bool=False
):
    ''' 
    gets new or exiting db connection,
    gets new cursor,
    executes query,
    commits,
    closes cursor,
    returns result
    '''
    db = db or get_db()
    cursor = db.cursor()

    # print(f'{stmt=}')
    # print(f'{args=}')
    cursor.execute(stmt, args)
    result = cursor.fetchall()

    if commit:
        db.commit()
    cursor.close()

    return result


def drop_table(name:str, db:MySQLConnection=None):
    ''' drops a table '''
    db = db or get_db()
    logger.info(f'dropping table: {name}')
    result = exec_statement(f'drop table if exists {name}', db)
    logger.info(f'{result = }')
