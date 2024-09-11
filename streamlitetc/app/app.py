import streamlit as st
from graphs import show_graphs
from predict import show_predict
from data import show_data

st.title("Football Match Predictor")


tab1, tab2, tab3 = st.tabs(["Data", "Graphs", "Predict"])


with tab1:
    show_data()

with tab2:
    show_graphs()

with tab3:
    show_predict()