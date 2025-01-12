import logging
import streamlit as st

from dashboard import pandasdal as dal
from dashboard import fixselect
from dashboard import helpers


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
helpers.fix_widgets_reload()
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
with st.sidebar:
    show_count = st.checkbox(
        label='show count',
        value=True,
        # key='link'
    )
    show_state = st.checkbox(
        label='show state',
        value=True,
        # key='link'
    )
###############################################################################
#
#   sidebar header filtri
#
###############################################################################
    st.header('Filtri')
    st.write('Usare le opzioni per filtrare i dati')
    
    link = st.checkbox(
        label='filtri collegati',
        value=True,
        # key='link'
    )

    st.button('reset filtri',
        on_click=helpers.reset_widgets
    )
###############################################################################
#
#   sidebar subheader geo
#
###############################################################################
    st.subheader('Geografia')
    
    prov = st.selectbox(                                                     # PROV
        label='seleziona una provincia',
        index=None if fixselect.FIX_INDEX else 0,
        options=dal.get_prov(df, link, **st.session_state),
        key='prov',
        placeholder='Non selezionato'
    )

    # st.sidebar.subheader('Luogo')
    luogo = st.selectbox(                                                   # LUOGO
        label='digita parte del luogo',
        index=None,
        options=dal.get_luogo(df, link, **st.session_state),
        key='luogo',
        placeholder='Non selezionato'
    )
###############################################################################
#
#   sidebar subheader biglietto
#
###############################################################################
    st.subheader('Biglietto')
    
    serie = st.selectbox(                                                   # SERIE
        label='seleziona una serie',
        index=None,
        options=dal.get_serie(df, link, **st.session_state),
        key='serie',
        placeholder='Non selezionato',
        # on_change=reset_geo
    )

    numero = st.selectbox(                                                  # NUMERO
        label='seleziona una numero',
        index=None,
        options=dal.get_numero(df, link, **st.session_state),
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
        options=dal.get_categoria(df, link, **st.session_state),
        key='categoria',
        placeholder='Non selezionato'
    )
    
    premio = st.selectbox(                                                  # PREMIO
        label='seleziona premio',
        index=None,
        options=dal.get_premio(df, link, **st.session_state),
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

st.dataframe(
    winners, 
    hide_index=True
)

if show_count:
    st.write(len(winners))

if show_state:
    st.session_state

helpers.console_space()
