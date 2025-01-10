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


with st.sidebar:
    st.header('Filtri')
    st.write('Usare le opzioni per filtrare i dati')
    
    link = st.checkbox(
        label='filtri collegati',
        value=True,
        key='link'
    )

    def reset_widgets():
        for el in st.session_state:
            if el not in ['link']:
                st.session_state[el] = None

    st.button('reset filtri',
        on_click=reset_widgets
    )



with st.sidebar:

    st.subheader('Geograficamente')

    prov = st.selectbox(
        label='seleziona una provincia',
        index=None,
        options=dal.get_prov(),
        key='prov',
        placeholder='Non selezionato'
    )

    # st.sidebar.subheader('Luogo')
    luogo = st.selectbox(
        label='digita parte del luogo',
        index=None,
        options=dal.get_luogo(prov=prov if link else None),
        key='luogo',
        placeholder='Non selezionato'
    )


with st.sidebar:
    st.subheader('Biglietto')
    
    def reset_geo():
        for elem in ['prov', 'luogo']:
            st.session_state[elem] = None
            
    
    serie = st.selectbox(
        label='seleziona una serie',
        index=None,
        options=dal.get_serie(),
        key='serie',
        placeholder='Non selezionato',
        on_change=reset_geo
    )

    numero = st.selectbox(
        label='seleziona una numero',
        index=None,
        options=dal.get_numero(serie=serie),
        key='numero',
        placeholder='Non selezionato',
        on_change=reset_geo
    )


with st.sidebar:
    st.subheader('Premio')
    categoria = st.selectbox(
        label='seleziona una categoria',
        index=None,
        options=dal.get_categoria(),
        key='categoria',
        placeholder='Non selezionato'
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
