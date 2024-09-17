import streamlit as st
from graphs import show_graphs
from predict import show_predict
from data import show_data
from compare import compare_teams  
import os

st.set_page_config(page_title="Football Match Predictor", layout="wide")

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

def navigate_to(page_name):
    st.session_state['page'] = page_name

def create_clickable_image(image_path, label, page_name):
    if not os.path.exists(image_path):
        st.error(f"Error: Image file not found: {image_path}")
        return

    st.image(image_path, caption=label, use_column_width=True)
    if st.button(label, use_container_width=True, key=page_name):
        navigate_to(page_name)

if st.session_state['page'] == 'home':
    st.title("Football Match Predictor")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_clickable_image("logos/data.png", "Data", "data")

    with col2:
        create_clickable_image("logos/analytics.png", "Graphs", "graphs")

    with col3:
        create_clickable_image("logos/ai.png", "Predict", "predict")

    with col4:
        create_clickable_image("logos/ai.png", "Compare", "compare")

elif st.session_state['page'] == 'data':
    show_data()
    if st.button("Back to Home"):
        navigate_to('home')

elif st.session_state['page'] == 'graphs':
    show_graphs()
    if st.button("Back to Home"):
        navigate_to('home')

elif st.session_state['page'] == 'predict':
    show_predict()
    if st.button("Back to Home"):
        navigate_to('home')

elif st.session_state['page'] == 'compare':
    compare_teams()  
    if st.button("Back to Home"):
        navigate_to('home')

st.markdown(
    """
    <style>
    .stApp {
        background: url("https://www.mirrormirror.be/media/pages/work/pro-league/7cb92b001c-1670404020/mirrormirror-pro-league-logo-boxed-1500x.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
