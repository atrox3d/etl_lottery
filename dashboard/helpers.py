import logging
import streamlit as st

import dashboard.fixselect as fixselect

logger = logging.getLogger(__name__)



def console_space(rows=10):
    ''' create some space in the console output '''

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
    if fixselect.CLEAR_STATE:
        st.session_state.clear()

    console_space()


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
    for elem in ['prov', 'luogo']:
        st.session_state[elem] = None