from enum import StrEnum
from typing import Union
import sqlite3
from mysql.connector import MySQLConnection
from sqlalchemy import Engine

from dbhelpers import dbfactory
from dbhelpers.mysql import db as mysql
from dbhelpers.sqlite import db as sqlite


DbSources = StrEnum('DbSources', 'SQLITE MYSQL')


def get_db(
        source       :DbSources, 
        sqlitepath   :str = None, 
        **mysql_args
) -> Union[sqlite3.Connection, MySQLConnection]:
    if source == DbSources.SQLITE:
        return sqlite.get_db(sqlitepath)
    elif source == DbSources.MYSQL:
        return mysql.get_db(**mysql_args)
    else:
        raise ValueError('source not recognized')


def get_engine(
        source       :DbSources, 
        sqlitepath   :str = None, 
        **mysql_args
) -> Engine:
    if source == DbSources.SQLITE:
        return sqlite.get_engine(sqlitepath)
    elif source == DbSources.MYSQL:
        return mysql.get_engine(**mysql_args)
    else:
        raise ValueError('source not recognized')


def get_connection_tester(
        source       :DbSources, 
) -> bool:
    if source == DbSources.SQLITE:
        return sqlite.test_connection
    elif source == DbSources.MYSQL:
        return mysql.test_connection
    else:
        raise ValueError('source not recognized')


#
# setup db
# TODO: move this to dbfactory
#
def setup_db(
    dbsource    : DbSources,
    config      : dict,
    sqlitepath  : str
) -> tuple[Union[sqlite3.Connection, MySQLConnection], Engine, callable, str]:
    
    if dbsource == dbfactory.DbSources.MYSQL:
        db = dbfactory.get_db(dbfactory.DbSources.MYSQL, **config)
        engine = dbfactory.get_engine(dbfactory.DbSources.MYSQL, **config)
        connection_tester = dbfactory.get_connection_tester(dbfactory.DbSources.MYSQL)
        dbdetails = f'{config["user"]}@{config["host"]}/{config["database"]}'
    
    elif dbsource == dbfactory.DbSources.SQLITE:
        db = dbfactory.get_db(dbfactory.DbSources.SQLITE, sqlitepath=sqlitepath)
        engine = dbfactory.get_engine(dbfactory.DbSources.SQLITE, sqlitepath=sqlitepath)
        connection_tester = dbfactory.get_connection_tester(dbfactory.DbSources.SQLITE)
        dbdetails = f'{sqlitepath}'
    
    else:
        raise NotImplementedError(f'{dbsource = }')
    return db, engine, connection_tester, dbdetails
