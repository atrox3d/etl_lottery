from mysql.connector import MySQLConnection
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import URL

from dbhelpers.config import build_config
from dbhelpers.db import get_db, test_connection, get_db_url


DB_NAME = 'testing'

config = build_config(database=DB_NAME)
db = get_db(config)

# winners = get_winners(db)


def get_connection_status() -> str:
    try:
        user, server, port = test_connection(config)
        connection_status = 'OK'
    except Exception as e:
        connection_status = 'ERRORE'
    return connection_status


def format_like(value, start:bool=False, middle:bool=False, end:bool=False) -> str:
    if middle:
        fmt = f'%{value}%'
    elif start:
        fmt = f'{value}%'
    elif end:
        fmt = f'%{value}'
    else:
        raise ValueError('at least one of start, middle, end is necessary')
    return fmt


def query_builder(sql:str, operator='AND', **args) -> str:
    conditions = []
    params = []
    
    print(f'{args = }')
    args = {condition:param for condition, param in args.items() if param}
    if args:
        for condition, param in args.items():
            if condition.endswith('__like'):
                condition = condition.replace('__like', ' like %s')
                conditions.append(condition)
                params.append(format_like(param, middle=True))
            else:
                conditions.append(f'{condition} = %s')
                params.append(param)
        
        sql = f'{sql} WHERE { f' {operator} ' .join(conditions)}'
        print(f'{sql = }')
        print(f'{conditions = }')
        print(f'{params = }')
        print(sql % tuple(params))
    else:
        print(sql)
    return sql, params


@st.cache_data
def get_winners(
            categoria:int=None, 
            luogo:str=None, 
            prov:str=None,
            serie:str=None,
            numero:str=None,
            premio:int=None
) -> pd.DataFrame:

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    # conditions = []
    params = []
    
    sql = 'SELECT * FROM lotteria'
    
    # if category is not None:
    #     conditions.append('categoria = %s')
    #     params.append(category)
    
    # if location is not None:
    #     conditions.append("luogo like %s")
    #     # params.append(f'%{location}%')
    #     params.append(format_like(location, middle=True))
        
    # if prov is not None:
    #     conditions.append('prov = %s')
    #     params.append(prov)
    
    # if conditions:
    #     sql = f'{sql} WHERE {" AND ".join(conditions)}'
    #     print(sql % tuple(params))
    sql, params = query_builder(
        sql, 
        categoria=categoria, 
        luogo=luogo, 
        prov=prov,
        serie=serie,
        numero=numero,
        premio=premio
    )
    return pd.read_sql(sql, engine, params=tuple(params))

@st.cache_data
def get_prov() -> pd.DataFrame:

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    # conditions = []
    params = []
    
    sql = 'select distinct Prov from lotteria order by prov'
        
    return pd.read_sql(sql, engine, params=tuple(params))

@st.cache_data
def get_luogo(prov:str=None) -> pd.DataFrame:

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    # conditions = []
    params = []
    
    sql = 'select distinct luogo from lotteria'
    
    # if prov is not None:
    #     conditions.append('prov = %s')
    #     params.append(prov)

    # if conditions:
    #     sql = f'{sql} WHERE {" AND ".join(conditions)}'
    sql, params = query_builder(sql, prov=prov)
    
    sql += ' order by luogo'
    
    if params:
        print(sql % tuple(params))
    else:
        print(sql)
        
    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data
def get_categoria() -> pd.DataFrame:

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    conditions = []
    params = []
    
    sql = 'select distinct categoria from lotteria order by categoria'
        
    return pd.read_sql(sql, engine, params=tuple(params))

