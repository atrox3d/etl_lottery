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



@st.cache_data
def get_winners(category:int=None, location:str=None, prov:str=None) -> pd.DataFrame:

    db_url = get_db_url(**config)
    engine = create_engine(db_url)
    
    conditions = []
    params = []
    
    sql = 'SELECT * FROM lotteria'
    
    if category is not None:
        conditions.append('categoria = %s')
        params.append(category)
    
    if location is not None:
        conditions.append("luogo like %s")
        params.append(f'%{location}%')
    
    if prov is not None:
        conditions.append('prov = %s')
        params.append(prov)
    
    if conditions:
        sql = f'{sql} WHERE {" AND ".join(conditions)}'
        print(sql % tuple(params))
    
    return pd.read_sql(sql, engine, params=tuple(params))
