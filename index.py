import logging
import pandas as pd
import numpy as np
import streamlit as st

from dashboard import dal

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(funcName)s | %(message)s'
)


st.title('Analisi lotteria italia')

st.write(f'''
        Dashboard per analisi vincite Lotteria Italia 2024 - 2025
        
        stato della connessione: {dal.get_connection_status()}
        ''')


st.sidebar.header('Filtri')
st.sidebar.write('Usare le opzioni per filtrare i dati')

def reset():
    for el in st.session_state:
        st.session_state[el] = None

st.sidebar.button('reset filtri',
    on_click=reset
)


st.sidebar.subheader('Geograficamente')
prov = st.sidebar.selectbox(
    label='seleziona una provincia',
    index=None,
    options=dal.get_prov(),
    key='prov'
)


# st.sidebar.subheader('Luogo')
luogo = st.sidebar.selectbox(
    label='digita parte del luogo',
    index=None,
    options=dal.get_luogo(prov=prov),
    key='luogo'
)

st.sidebar.subheader('Biglietto')
categoria = st.sidebar.selectbox(
    label='seleziona una categoria',
    index=None,
    options=dal.get_categoria(),
    key='categoria'
)

serie = st.sidebar.selectbox(
    label='seleziona una serie',
    index=None,
    options=dal.get_serie(),
    key='serie'
)

numero = st.sidebar.selectbox(
    label='seleziona una numero',
    index=None,
    options=dal.get_numero(serie=serie),
    key='numero'
)




# winners = get_winners(category=3, prov='MI')
winners = dal.get_winners(
    prov=prov, 
    luogo=luogo, 
    categoria=categoria,
    serie=serie,
    numero=numero
)
# st.write(winners
        # .head()
    # )
st.dataframe(
    winners, 
    hide_index=True
)
st.write(len(winners))

# st.session_state
if st.button('stop'):
    st.stop()