import pandas as pd
import numpy as np
import streamlit as st

from dbhelpers.config import build_config
from dbhelpers.db import get_db, test_connection
from dashboard.dal import get_winners
DB_NAME = 'testing'
config = build_config(database=DB_NAME)

try:
    user, server, port = test_connection(config)
    connection_status = 'OK'
except Exception as e:
    connection_status = 'ERRORE'
    
db = get_db(config)
winners = get_winners(db)


st.title('Analisi lotteria italia')

st.write(f'''
        Dashboard per analisi vincite Lotteria Italia 2024 - 2025
        
        stato della connessione: {connection_status}
        ''')

st.write(winners.head())



st.sidebar.header('Filtri')
st.sidebar.write('Usare le opzioni per filtrare i dati')

st.sidebar.subheader('Provincia')

st.sidebar.subheader('Luogo')


