# https://medium.com/streamlit/paginating-dataframes-with-streamlit-2da29b080920

import streamlit as st
import pandas as pd
import numpy as np

from pagination import data
from pagination import interface

file_path = st.file_uploader('Select CSV', type=['csv'])

if file_path:
    df = data.load_csv(file_path)

    interface.paginated_df(df)

