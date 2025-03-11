import logging
import streamlit as st
import pandas as pd

from dashboard import fixselect

logger = logging.getLogger(__name__)


def logger_console_space(rows=5):
    ''' create some space in the console output '''
    
    for _ in range(rows):
        logger.info('')


def reset_widgets():
    ''' reset widgets '''
    
    logger.info('RESETTING WIDGETS')
    for el in st.session_state:
        if el not in ['link']:
            logger.debug(f'resetting {el}')
            del st.session_state[el]
    if fixselect.CLEAR_STATE:
        st.session_state.clear()
    logger_console_space()


def fix_widgets_reload():
    ''' Interrupting the widget clean-up process 
        https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
    '''
    if not fixselect.FIX_WIDGETS:
        # returning immediately causes select boxes do not keep values
        # while st.session_state does
        logger.warning('NOT SELF ASSIGNING SESSION STATE')
        return
    for k, v in st.session_state.items():
        st.session_state[k] = v


def reset_geo():
    ''' resets geo section of location widgets '''
    for elem in ['prov', 'luogo']:
        st.session_state[elem] = None
