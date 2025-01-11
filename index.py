import logging
import pandas as pd
import numpy as np
import streamlit as st
from traitlets import default

# from dashboard import sqldal as dal
from dashboard import pandasdal as dal


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(funcName)s | %(message)s'
)


def console_space(rows=10):
    for _ in range(rows):
        logger.info('') 
#
#   title
#
st.title('Analisi lotteria italia')
st.write(f'''
        Dashboard per analisi vincite Lotteria Italia 2024 - 2025
        
        stato della connessione: {dal.get_connection_status()}
        ''')
#
#   sidebar header
#
with st.sidebar:
    
    st.header('Filtri')
    st.write('Usare le opzioni per filtrare i dati')
    
    link = st.checkbox(
        label='filtri collegati',
        value=True,
        # key='link'
    )

    def reset_widgets():
        ''' reset widgets '''
        
        logger.info('RESETTING WIDGETS')
        for el in st.session_state:
            if el not in ['link']:
                logger.debug(f'resetting {el}')
                st.session_state[el] = None
        
        console_space()
        
        
        
    st.button('reset filtri',
        on_click=reset_widgets
    )


df  = dal.get_winners().copy()
#
#   sidebar filters
#
with st.sidebar:
    #
    #   sidebar subheader geo
    #
    st.subheader('Geograficamente')

    prov = st.selectbox(                                                     # PROV
        label='seleziona una provincia',
        # index=None,
        options=dal.get_prov(df, link,
                            **st.session_state
        ),
        key='prov',
        placeholder='Non selezionato'
    )

    # st.sidebar.subheader('Luogo')
    luogo = st.selectbox(                                                   # LUOGO
        label='digita parte del luogo',
        # index=None,
        options=dal.get_luogo(df, link, 
                            **st.session_state
        ),
        key='luogo',
        placeholder='Non selezionato'
    )

with st.sidebar:
    #
    #   sidebar subheader biglietto
    #
    st.subheader('Biglietto')
    
    def reset_geo():
        for elem in ['prov', 'luogo']:
            st.session_state[elem] = None
            
    
    serie = st.selectbox(                                                   # SERIE
        label='seleziona una serie',
        # index=None,
        options=dal.get_serie(df, link,
                            **st.session_state
        ),
        key='serie',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )

    numero = st.selectbox(                                                  # NUMERO
        label='seleziona una numero',
        # index=None,
        options=dal.get_numero(df, link, 
                            **st.session_state
        ),
        key='numero',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )


with st.sidebar:
    #
    #   sidebar subheader premio
    #
    st.subheader('Premio')
    
    categoria = st.selectbox(                                               # CATEGORIA
        label='seleziona una categoria',
        # index=None,
        options=dal.get_categoria(df, link, 
                            **st.session_state
        ),
        key='categoria',
        placeholder='Non selezionato'
    )
    
    premio = st.selectbox(                                                  # PREMIO
        label='seleziona premio',
        # index=None,
        options=dal.get_premio(df, link, 
                            **st.session_state
        ),
        key='premio',
        placeholder='Non selezionato'
    )

#
#   TABLE
#

# winners = get_winners(category=3, prov='MI')
winners = dal.get_winners(
    prov=prov, 
    luogo=luogo, 
    categoria=categoria,
    serie=serie,
    numero=numero,
    premio=premio
)
# st.write(winners
        # .head()
    # )
st.dataframe(
    winners, 
    hide_index=True
)
st.write(len(winners))

st.session_state

console_space()
