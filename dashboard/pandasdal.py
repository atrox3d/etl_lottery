# from mysql.connector import MySQLConnection
import logging
from typing import Callable
import pandas as pd
import streamlit as st
from sqlalchemy import Engine, text

from dbhelpers.querybuilder import filter_dict_nulls, query_builder

# from dbhelpers.mysql import config as _config
# from dbhelpers.mysql import db

logger = logging.getLogger(__name__)

CACHE_TTL = None


def get_connection_status(test_connection:Callable) -> str:
    ''' get connection status as string'''
    
    if test_connection():
        connection_status = 'OK'
    else:
        connection_status = 'ERRORE'
    
    logger.info(f'connection status: {connection_status}')
    return connection_status


def filter_dict_df_keys(df:pd.DataFrame, **state) -> dict:
    ''' filter df values based on state keys '''
    return {k:v for k, v in state.items() if k in df.columns}


@st.cache_data
def get_empty_winners(_engine:Engine) -> pd.DataFrame:
    ''' utility to get just mysql table column names '''
    empty_df = pd.read_sql('SELECT * FROM lotteria LIMIT 0;', _engine, index_col='index')
    return empty_df


@st.cache_data(ttl=CACHE_TTL)
def get_winners( _engine:Engine, **fields ) -> pd.DataFrame:
    ''' get filtered df from db '''
    
    # prepare query for pandas df
    logger.debug(f'{fields = }')
    params = filter_dict_df_keys(
            get_empty_winners(_engine),
            **fields
    )
    logger.debug(f'{params = }')

    params = filter_dict_nulls(
            **params
    )
    logger.debug(f'{params = }')
    
    sql, params = query_builder(
        'SELECT * FROM lotteria', 
        **params
    )
    logger.debug(f'{params = }')
    logger.debug(f'{sql = }')
    
    # run query and return result df
    df =  pd.read_sql(text(sql), _engine, params=params, index_col='index')
    logger.debug(df)
    logger.debug(len(df))
    
    return df


@st.cache_data(ttl=CACHE_TTL)
def get_field(name:str, df:pd.DataFrame, link:bool, **kwargs) -> pd.DataFrame:
    ''' get df column applying conditions '''
    
    logger.debug(f'{name = }, {link = }, {kwargs = }')
    
    filtered_kwargs = filter_dict_df_keys(df, **kwargs)
    logger.debug(f'{name = }, {link = }, {filtered_kwargs = }')
    
    # filter df if linked option enabled in sidebar
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
