import logging
import pandas as pd
import numpy as np
import streamlit as st
from traitlets import default

# from dashboard import sqldal as dal
from dashboard import pandasdal as dal


def console_space(rows=10):
    ''' create some space in the console output '''
    
    return
    for _ in range(rows):
        logger.info('') 


def reset_widgets():
    ''' reset widgets '''
    logger.info('RESETTING WIDGETS')
    for el in st.session_state:
        if el not in ['link']:
            logger.info(f'resetting {el}')
            del st.session_state[el]
            # print(st.session_state[el])
            # st.session_state[el] = None
        
    st.session_state.clear()
    
    console_space()


def fix_widgets_reload():
    ''' Interrupting the widget clean-up process 
        https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
    '''
    logger.warning('NOT SELF ASSIGNING SESSION STATE')
    return
    for k, v in st.session_state.items():
        st.session_state[k] = v
###############################################################################
#
#   setup logging and dataframe
#
###############################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(funcName)s | %(message)s'
)
df  = dal.get_winners().copy()
fix_widgets_reload()
###############################################################################
#
#   title
#
###############################################################################
st.title('Analisi lotteria italia')
st.write(f'''
    Dashboard per analisi vincite Lotteria Italia 2024 - 2025
    
    stato della connessione: {dal.get_connection_status()}
''')
###############################################################################
#
#   sidebar header filtri
#
###############################################################################
with st.sidebar:
    
    st.header('Filtri')
    st.write('Usare le opzioni per filtrare i dati')
    
    link = st.checkbox(
        label='filtri collegati',
        value=True,
        # key='link'
    )

    st.button('reset filtri',
        on_click=reset_widgets
    )
###############################################################################
#
#   sidebar subheader geo
#
###############################################################################
    st.subheader('Geograficamente')
    
    prov = st.selectbox(                                                     # PROV
        label='seleziona una provincia',
        index=None,
        options=dal.get_prov(df, link,
                            **st.session_state
        ),
        key='prov',
        placeholder='Non selezionato'
    )

    # st.sidebar.subheader('Luogo')
    luogo = st.selectbox(                                                   # LUOGO
        label='digita parte del luogo',
        index=None,
        options=dal.get_luogo(df, link, 
                            **st.session_state
        ),
        key='luogo',
        placeholder='Non selezionato'
    )
###############################################################################
#
#   sidebar subheader biglietto
#
###############################################################################
    st.subheader('Biglietto')
    
    def reset_geo():
        for elem in ['prov', 'luogo']:
            st.session_state[elem] = None
            
    
    serie = st.selectbox(                                                   # SERIE
        label='seleziona una serie',
        index=None,
        options=dal.get_serie(df, link,
                            **st.session_state
        ),
        key='serie',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )

    numero = st.selectbox(                                                  # NUMERO
        label='seleziona una numero',
        index=None,
        options=dal.get_numero(df, link, 
                            **st.session_state
        ),
        key='numero',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )
###############################################################################
#
#   sidebar subheader premio
#
###############################################################################
    st.subheader('Premio')
    
    categoria = st.selectbox(                                               # CATEGORIA
        label='seleziona una categoria',
        index=None,
        options=dal.get_categoria(df, link, 
                            **st.session_state
        ),
        key='categoria',
        placeholder='Non selezionato'
    )
    
    premio = st.selectbox(                                                  # PREMIO
        label='seleziona premio',
        index=None,
        options=dal.get_premio(df, link, 
                            **st.session_state
        ),
        key='premio',
        placeholder='Non selezionato'
    )
###############################################################################
#
#   TABLE
#
###############################################################################

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
