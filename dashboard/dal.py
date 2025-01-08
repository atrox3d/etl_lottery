from mysql.connector import MySQLConnection
import pandas as pd
import numpy as np
import streamlit as st

from dbhelpers.config import build_config
from dbhelpers.db import get_db, test_connection
from dashboard.dal import get_winners

DB_NAME = 'testing'
config = build_config(database=DB_NAME)
db = get_db(config)

def get_connection_status():
    try:
        user, server, port = test_connection(config)
        connection_status = 'OK'
    except Exception as e:
        connection_status = 'ERRORE'
    return connection_status

winners = get_winners(db)



    
@st.cache_data
def get_winners(location:str=None, prov:str=None) -> pd.DataFrame:
    sql = """
    SELECT *
    FROM lotteria
    """
    return pd.read_sql(sql, db)
