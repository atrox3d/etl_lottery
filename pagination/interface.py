import logging
import streamlit as st
import pandas as pd
import numpy as np

from pagination import data


logger = logging.getLogger(__name__)


def paginated_df(
        df:pd.DataFrame, 
        sort_menu:bool=True, 
        navigation_menu:bool=True,
        hide_index:bool=True
):
    '''create a paginated interface for a dataframe'''
    
    for x in df.head().to_string().split('\n'):
        logger.info(x)
    logger.info(f'{len(df) = }')

    df = df.reset_index(drop=True)
    
    # display sort menu if enabled
    if sort_menu:
        upleft_menu, upcenter_menu, upright_menu = st.columns(3)

        with upleft_menu:
            sort_yn = st.toggle('Ordinamento dati', value=sort_menu)
            
            if sort_yn:
                
                with upcenter_menu:
                    sort_field = st.selectbox('Ordina per', options=df.columns)
                
                with upright_menu:
                    sort_dir = st.radio('Direzione', options=['⬆️', '⬇️'], horizontal=True)
                
                df = df.sort_values(
                    by=sort_field, 
                    ascending=sort_dir=='⬆️', 
                    ignore_index=True
                )
    
    # the paginated df table
    paginated = st.container()
    
    # display navigatin menu if enabled
    if navigation_menu:
        dnleft_menu, dncenter_menu, dnright_menu = st.columns((4, 1, 1))
        
        with dnright_menu:
            batch_size = st.selectbox('Righe per pag.', options=[10, 25, 50, 100])
        
        with dncenter_menu:
            int_pages = int(len(df) / batch_size)
            total_pages = (int_pages if int_pages > 0 else 1)
            
            # fix "current page index overflow" when filtering df and current page of the view 
            # is already greater than the length of the filtered df
            if st.session_state.get('page') is None:
                st.session_state.page = 1
            if st.session_state.page > total_pages:
                st.session_state.page = total_pages
            
            current_page = st.number_input(
                'Pag.', min_value=1, max_value=total_pages, step=1,
                key='page'
                )
                
        with dnleft_menu:
            st.markdown(f'Pag. **{current_page}** di **{total_pages}** - (totale: {len(df)} records)')
            
            left, right = st.columns(2)
            
            def previous_page():
                if st.session_state.page > 1:
                    st.session_state.page -= 1

            def next_page():
                if st.session_state.page < total_pages:
                    st.session_state.page += 1
            
            with left:
                st.button(
                    '⬅️', 
                    on_click=previous_page,
                    disabled=current_page==1
                )
            with right:
                st.button(
                    '➡️', 
                    on_click=next_page,
                    disabled=current_page==total_pages
                )
        
        # pagination display logic
        splitdf = data.split_df(df, batch_size)
        logger.info('-'*50)
        WIDTH = 20
        logger.debug(f'{len(splitdf) = :>{WIDTH}}')
        logger.debug(f'{int_pages = :>{WIDTH}}')
        logger.debug(f'{total_pages = :>{WIDTH}}')
        logger.debug(f'{st.session_state.page = :>{WIDTH}}')
        logger.debug(f'{current_page = :>{WIDTH}}')
        logger.debug('-'*50)
        if len(splitdf):
            paginated.dataframe(
                data=splitdf[st.session_state.page-1],   #FIXME: IndexError: list index out of range
                use_container_width=True,
                hide_index=hide_index,
            )
        else:
            paginated.dataframe(
                data=df.head(0),
                use_container_width=True,
                hide_index=hide_index,
            )


