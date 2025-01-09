import pandas as pd
import numpy as np
import streamlit as st

from dashboard import dal


st.title('Analisi lotteria italia')

st.write(f'''
        Dashboard per analisi vincite Lotteria Italia 2024 - 2025
        
        stato della connessione: {dal.get_connection_status()}
        ''')


st.sidebar.header('Filtri')
st.sidebar.write('Usare le opzioni per filtrare i dati')

st.sidebar.subheader('Geograficamente')
provence = st.sidebar.selectbox(
    label='seleziona una provincia',
    index=None,
    options=dal.get_provence()
)

# st.sidebar.subheader('Luogo')
location = st.sidebar.selectbox(
    label='digita parte del luogo',
    index=None,
    options=dal.get_location(prov=provence)
)

st.sidebar.subheader('Biglietto')
category = st.sidebar.selectbox(
    label='seleziona una categoria',
    index=None,
    options=dal.get_category()
)




# winners = get_winners(category=3, prov='MI')
winners = dal.get_winners(prov=provence, location=location, category=category)
st.write(winners.head())
st.write(len(winners))

