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
CACHE_TTL = None
config = build_config(database=DB_NAME)
# db = get_db(config)
# winners = get_winners(db)


def get_connection_status() -> str:
    ''' get connection status as string'''
    
    try:
        user, server, port = test_connection(config)
        connection_status = 'OK'
    except Exception as e:
        connection_status = 'ERRORE'
    
    logger.info(f'connection status: {connection_status}')
    return connection_status


def format_like(value, start:bool=False, middle:bool=False, end:bool=False) -> str:
    ''' format sql like value to parametrize queries '''
    
    if middle:
        fmt = f'%{value}%'
    elif start:
        fmt = f'{value}%'
    elif end:
        fmt = f'%{value}'
    else:
        raise ValueError('at least one of start, middle, end is necessary')
    logger.debug(f'{fmt = }')
    return fmt


def query_builder(sql:str, operator='AND', **kwargs) -> str:
    ''' dynamically creates queries vases on kwargs '''
    
    conditions = []
    params = []
    
    kwargs = filter_dict_nulls(**kwargs)
    logger.info(f'{kwargs = }')
    
    if kwargs:
        for condition, param in kwargs.items():
            if condition.endswith('__like'):
                condition = condition.replace('__like', ' like %s')
                conditions.append(condition)
                params.append(format_like(param, middle=True))
            else:
                conditions.append(f'{condition} = %s')
                params.append(param)
        
        sql = f'{sql} WHERE { f' {operator} ' .join(conditions)}'
        logger.debug(f'{sql = }')
        logger.debug(f'{conditions = }')
        logger.debug(f'{params = }')
        logger.info(sql % tuple(params))
    else:
        logger.info(sql)
    return sql, params


def filter_dict_nulls(**kwargs) -> dict:
    return {k:v for k, v in kwargs.items() if v}


def filter_dict_df_keys(df:pd.DataFrame, **state) -> dict:
    return {k:v for k, v in state.items() if k in df.columns}


@st.cache_data
def get_empty_winners() -> pd.DataFrame:
    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    empty_df = pd.read_sql('SELECT * FROM lotteria LIMIT 0;', engine, index_col='index')
    
    return empty_df

@st.cache_data(ttl=CACHE_TTL)
def get_winners(
            # categoria:int=None, 
            # luogo:str=None, 
            # prov:str=None,
            # serie:str=None,
            # numero:str=None,
            # premio:int=None
            **fields
) -> pd.DataFrame:
    ''' get filtered df from mysql db '''
    
    db_url = get_db_url(**config)
    engine = create_engine(db_url)

    logger.debug(f'{fields = }')
    params = filter_dict_df_keys(
            get_empty_winners(),
            **fields
    )
    logger.debug(f'{params = }')

    params = filter_dict_nulls(
            **params
            # categoria=categoria, 
            # luogo=luogo, 
            # prov=prov,
            # serie=serie,
            # numero=numero,
            # premio=premio
    )
    logger.debug(f'{params = }')

    
    sql, params = query_builder(
        'SELECT * FROM lotteria', 
        **params
        # categoria=categoria, 
        # luogo=luogo, 
        # prov=prov,
        # serie=serie,
        # numero=numero,
        # premio=premio
    )
    logger.debug(f'{params = }')
    logger.debug(f'{sql = }')
    
    df =  pd.read_sql(sql, engine, params=tuple(params), index_col='index')
    logger.debug(df)
    logger.debug(len(df))
    
    return df


@st.cache_data(ttl=CACHE_TTL)
def get_field(name:str, df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' get df column applying conditions '''
    
    logger.debug(f'{name = }, {link = }, {kwargs = }')
    
    filtered_kwargs = filter_dict_df_keys(df, **kwargs)
    logger.debug(f'{name = }, {link = }, {filtered_kwargs = }')
    
    if link:
        for col, val in filtered_kwargs.items():
            if val is not None:
                df = df[df[col]==val]
    return df[name]


@st.cache_data(ttl=CACHE_TTL)
def get_prov(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('prov', df, link, **kwargs).sort_values().unique()


@st.cache_data(ttl=CACHE_TTL)
def get_luogo(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('luogo', df, link, **kwargs).sort_values().unique()


@st.cache_data(ttl=CACHE_TTL)
def get_serie(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('serie', df, link, **kwargs).sort_values().unique()


@st.cache_data(ttl=CACHE_TTL)
def get_numero(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('numero', df, link, **kwargs).sort_values().unique()


@st.cache_data(ttl=CACHE_TTL)
def get_categoria(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('categoria', df, link, **kwargs).sort_values().unique()


@st.cache_data(ttl=CACHE_TTL)
def get_premio(df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' data helper '''
    
    return get_field('premio', df, link, **kwargs).sort_values().unique()
