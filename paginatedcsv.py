import streamlit as st
import pandas as pd
import numpy as np

from pagination import data

file_path = st.file_uploader('Select CSV', type=['csv'])

if file_path:
    df = data.load_csv(file_path)
    splitdf = data.split_df(df, 10)

    splitdf[0]



# st.write(type(splitdf))
