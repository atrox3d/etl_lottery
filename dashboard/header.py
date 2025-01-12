import pandas as pd
import streamlit as st
from dashboard import helpers, fixselect, pandasdal as dal

def display_options() -> tuple[bool, bool]:
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
    
    return show_count, show_state


def filter_options() -> bool:
    
    link = st.checkbox( label='filtri collegati', value=True, )
    
    st.button('reset filtri',
        on_click=helpers.reset_widgets
    )
    
    return link


def geo_filters(df:pd.DataFrame, link:bool) -> tuple[str, str]:
    prov = st.selectbox(                                                     # PROV
        label='seleziona una provincia',
        index=None if fixselect.FIX_INDEX else 0,
        options=dal.get_prov(df, link, **st.session_state),
        key='prov',
        placeholder='Non selezionato'
    )

    luogo = st.selectbox(                                                   # LUOGO
        label='digita parte del luogo',
        index=None,
        options=dal.get_luogo(df, link, **st.session_state),
        key='luogo',
        placeholder='Non selezionato'
    )
    
    return prov, luogo


def ticket_filters(df:pd.DataFrame, link:bool) -> tuple[str, str]:
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
    
    return serie, numero


def prize_filters(df:pd.DataFrame, link:bool) -> tuple[str, str]:
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
    
    return categoria, premio

