import streamlit as st
import pandas as pd

def show_data():
    st.write("## Current Data")
    st.write("Here you can see the current data.")
    
    df = pd.read_csv("B12425.csv")
    df = df.dropna()
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG',
       'HTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY',
       'HR', 'AR']]
    
    
    if st.button("Show Data Info"):
        st.write("### Data Sample")
        st.write(df)

    if st.button("Show Column Info"):
        st.write("### Column Info")
        with open("column_info.txt", "r") as file:
            st.write(file.read())
        
    