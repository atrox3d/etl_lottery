# from mysql.connector import MySQLConnection
import logging
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import URL

from dbhelpers.config import build_config
from dbhelpers.db import get_db, test_connection, get_db_url

logger = logging.getLogger(__name__)
DB_NAME = 'testing'

config = build_config(database=DB_NAME)
# db = get_db(config)

# winners = get_winners(db)

CACHE_TTL = 0

def get_connection_status() -> str:
    return 'X'
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
    
    logger.info(f'{args = }')
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
        logger.info(f'{sql = }')
        logger.info(f'{conditions = }')
        logger.info(f'{params = }')
        logger.info(sql % tuple(params))
    else:
        logger.info(sql)
    return sql, params


@st.cache_data(ttl=CACHE_TTL)
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

    logger.debug(dict(
        categoria=categoria, 
        luogo=luogo, 
        prov=prov,
        serie=serie,
        numero=numero,
        premio=premio

    ))
    
    sql, params = query_builder(
        'SELECT * FROM lotteria', 
        categoria=categoria, 
        luogo=luogo, 
        prov=prov,
        serie=serie,
        numero=numero,
        premio=premio
    )
    return pd.read_sql(sql, engine, params=tuple(params), index_col='index')

@st.cache_data(ttl=CACHE_TTL)
def get_field(name:str, df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    # df = df if link else get_winners()
    logger.debug(name)
    logger.debug(kwargs)
    if link:
        for col, val in kwargs.items():
            if val is not None:
                df = df[df[col]==val]
    return df[name]


@st.cache_data(ttl=CACHE_TTL)
def get_prov(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    # df = df if link else get_winners()
    # return df.Prov.sort_values().unique()
    return get_field('prov', df, link, **kwargs).sort_values().unique()

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    params = []
    sql = 'select distinct Prov from lotteria order by prov'
        
    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data(ttl=CACHE_TTL)
def get_luogo(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    return get_field('luogo', df, link, **kwargs).sort_values().unique()


    df = df if link else get_winners()
    for col, val in kwargs.items():
        if val is not None:
            df = df[df[col]==val]
    return df.Luogo
    
    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    sql, params = query_builder(
        'select distinct luogo from lotteria', 
        prov=prov
    )
    sql += ' order by luogo'

    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data(ttl=CACHE_TTL)
def get_serie(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    return get_field('serie', df, link, **kwargs).sort_values().unique()

    df = df if link else get_winners()
    return df.Serie

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    params = []
    sql = 'select distinct serie from lotteria order by serie'
        
    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data(ttl=CACHE_TTL)
def get_numero(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    return get_field('numero', df, link, **kwargs).sort_values().unique()

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    params = []
    sql, params = query_builder(
        'select numero from lotteria',
        serie=serie
    )
    sql += ' order by numero'
    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data(ttl=CACHE_TTL)
def get_categoria(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    return get_field('categoria', df, link, **kwargs).sort_values().unique()

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    params = []
    sql = 'select distinct categoria from lotteria order by categoria'
        
    return pd.read_sql(sql, engine, params=tuple(params))


@st.cache_data(ttl=CACHE_TTL)
def get_premio(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:

    return get_field('premio', df, link, **kwargs).sort_values().unique()
