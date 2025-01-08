import pandas as pd
import numpy as np
import streamlit as st

from dashboard.dal import get_connection_status, get_winners

winners = get_winners(category=2)

st.title('Analisi lotteria italia')

st.write(f'''
        Dashboard per analisi vincite Lotteria Italia 2024 - 2025
        
        stato della connessione: {get_connection_status()}
        ''')

st.write(winners.head())



st.sidebar.header('Filtri')
st.sidebar.write('Usare le opzioni per filtrare i dati')

st.sidebar.subheader('Provincia')

st.sidebar.subheader('Luogo')


