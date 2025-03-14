import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_csv(file_path:str) -> pd.DataFrame:
    '''get df from csv file'''
    
    df = pd.read_csv(file_path)
    return df


@st.cache_data
def split_df(df:pd.DataFrame, rows:int) -> list[pd.DataFrame]:
    '''splits df into paginated list of dfs'''
    
    splitdf = [df.iloc[i: i+rows -1, :] for i in range(
                0, len(df), rows)
    ]
    
    return splitdf
