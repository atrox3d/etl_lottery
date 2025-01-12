import streamlit as st
import pandas as pd
import numpy as np

from pagination import data


def paginated_df(df:pd.DataFrame):
    
    upleft_menu, upcenter_menu, upright_menu = st.columns(3)

    with upleft_menu:
        sort_yn = st.radio('Sort Data', options=['Yes', 'No'], horizontal=True, index=1)
        
        if sort_yn == 'Yes':
            
            with upcenter_menu:
                sort_field = st.selectbox('Sort by', options=df.columns)
            
            with upright_menu:
                sort_dir = st.radio('Direction', options=['⬆️', '⬇️'], horizontal=True)
            
            df = df.sort_values(by=sort_field, ascending=sort_dir=='⬆️', ignore_index=True)
    
    paginated = st.container()
    
    dnleft_menu, dncenter_menu, dnright_menu = st.columns((4, 1, 1))
    
    with dnright_menu:
        batch_size = st.selectbox('Page Size', options=[10, 25, 50, 100])
    
    with dncenter_menu:
        int_pages = int(len(df) / batch_size)
        total_pages = (int_pages if int_pages > 0 else 1)
        current_page = st.number_input(
            'Page', min_value=1, max_value=total_pages, step=1,
            key='page'
            )
            
    with dnleft_menu:
        st.markdown(f'Page **{current_page}** of **{total_pages}**')
        
        left, right = st.columns(2)
        
        def left_page():
            if st.session_state.page > 1:
                st.session_state.page -= 1

        def right_page():
            if st.session_state.page < batch_size:
                st.session_state.page += 1
        
        with left:
            st.button('left', on_click=left_page)
        with right:
            st.button('right', on_click=right_page)

    splitdf = data.split_df(df, batch_size)
    paginated.dataframe(data=splitdf[current_page-1], use_container_width=True)
