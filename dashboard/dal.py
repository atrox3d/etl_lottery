from mysql.connector import MySQLConnection
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def get_winners(db:MySQLConnection) -> pd.DataFrame:
    sql = """
    SELECT *
    FROM lotteria
    """
    return pd.read_sql(sql, db)
