from enum import StrEnum
from typing import Union
import sqlite3
from mysql.connector import MySQLConnection

from dbhelpers.mysql import db as mysql
from dbhelpers.sqlite import db as sqlite


DbSources = StrEnum('DbSources', 'SQLITE MYSQL')


def get_db(
        source       :DbSources, 
        sqlitepath   :str, 
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
        sqlitepath   :str, 
        **mysql_args
) -> Union[sqlite3.Connection, MySQLConnection]:
    if source == DbSources.SQLITE:
        return sqlite.get_engine(sqlitepath)
    elif source == DbSources.MYSQL:
        return mysql.get_engine(**mysql_args)
    else:
        raise ValueError('source not recognized')
