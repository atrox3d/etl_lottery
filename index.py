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
prov = st.sidebar.selectbox(
    label='seleziona una provincia',
    index=None,
    options=dal.get_prov()
)

# st.sidebar.subheader('Luogo')
luogo = st.sidebar.selectbox(
    label='digita parte del luogo',
    index=None,
    options=dal.get_luogo(prov=prov)
)

st.sidebar.subheader('Biglietto')
categoria = st.sidebar.selectbox(
    label='seleziona una categoria',
    index=None,
    options=dal.get_categoria()
)




# winners = get_winners(category=3, prov='MI')
winners = dal.get_winners(prov=prov, luogo=luogo, categoria=categoria)
st.write(winners.head())
st.write(len(winners))

