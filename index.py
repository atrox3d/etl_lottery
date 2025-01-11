import logging
import pandas as pd
import numpy as np
import streamlit as st

# from dashboard import sqldal as dal
from dashboard import pandasdal as dal


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(funcName)s | %(message)s'
)
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
        key='link'
    )

    def reset_widgets():
        ''' reset widgets '''
        
        logger.info('RESETTING WIDGETS')
        for el in st.session_state:
            if el not in ['link']:
                st.session_state[el] = None

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
        index=None,
        options=dal.get_prov(df, link,
                            # Luogo=st.session_state.get('luogo'), 
                            # Serie=st.session_state.get('serie'), 
                            # Numero=st.session_state.get('numero'), 
                            # Categoria=st.session_state.get('categoria'), 
                            # Premio=st.session_state.get('premio')
        ),
        key='prov',
        placeholder='Non selezionato'
    )

    # st.sidebar.subheader('Luogo')
    luogo = st.selectbox(                                                   # LUOGO
        label='digita parte del luogo',
        index=None,
        options=dal.get_luogo(df, link, 
                            prov=st.session_state.get('prov'),
                            # Serie=st.session_state.get('serie'), 
                            # Numero=st.session_state.get('numero'), 
                            # Categoria=st.session_state.get('categoria'), 
                            # Premio=st.session_state.get('premio')
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
        index=None,
        options=dal.get_serie(df, link,
                            # Prov=st.session_state.get('prov'),
                            # Luogo=st.session_state.get('luogo'), 
                            # Numero=st.session_state.get('numero'), 
                            # Categoria=st.session_state.get('categoria'), 
                            # Premio=st.session_state.get('premio')
        ),
        key='serie',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )

    numero = st.selectbox(                                                  # NUMERO
        label='seleziona una numero',
        index=None,
        options=dal.get_numero(df, link, 
                            # Prov=st.session_state.get('prov'),
                            # Luogo=st.session_state.get('luogo'), 
                            # Serie=st.session_state.get('serie'), 
                            # Categoria=st.session_state.get('categoria'), 
                            # Premio=st.session_state.get('premio')
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
        index=None,
        options=dal.get_categoria(df, link, 
                            # Prov=st.session_state.get('prov'),
                            # Luogo=st.session_state.get('luogo'), 
                            # Serie=st.session_state.get('serie'), 
                            # Numero=st.session_state.get('numero'), 
                            # Premio=st.session_state.get('premio')
        ),
        key='categoria',
        placeholder='Non selezionato'
    )
    
    premio = st.selectbox(                                                  # PREMIO
        label='seleziona premio',
        index=None,
        options=dal.get_premio(df, link, 
                            # Prov=st.session_state.get('prov'),
                            # Luogo=st.session_state.get('luogo'), 
                            # Serie=st.session_state.get('serie'), 
                            # Numero=st.session_state.get('numero'), 
                            # Categoria=st.session_state.get('categoria'), 
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

