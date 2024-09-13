import streamlit as st
from graphs import show_graphs
from predict import show_predict
from data import show_data
from compare import compare_teams  # compare_teams fonksiyonunu içe aktar
import os

# Set the configuration for the Streamlit app
st.set_page_config(page_title="Football Match Predictor", layout="wide")

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Function to navigate to different pages
def navigate_to(page_name):
    st.session_state['page'] = page_name

# Function to create clickable images for navigation
def create_clickable_image(image_path, label, page_name):
    if not os.path.exists(image_path):
        st.error(f"Error: Image file not found: {image_path}")
        return

    # Display image and create a button for navigation
    st.image(image_path, caption=label, use_column_width=True)
    if st.button(label, use_container_width=True, key=page_name):
        navigate_to(page_name)

# Home page with clickable images for navigation
if st.session_state['page'] == 'home':
    st.title("Football Match Predictor")

    # Creating 4 columns for displaying clickable images
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_clickable_image("logos/data.png", "Data", "data")

    with col2:
        create_clickable_image("logos/analytics.png", "Graphs", "graphs")

    with col3:
        create_clickable_image("logos/ai.png", "Predict", "predict")

    with col4:
        create_clickable_image("logos/ai.png", "Compare", "compare")

# Data page
elif st.session_state['page'] == 'data':
    show_data()
    if st.button("Back to Home"):
        navigate_to('home')

# Graphs page
elif st.session_state['page'] == 'graphs':
    show_graphs()
    if st.button("Back to Home"):
        navigate_to('home')

# Predict page
elif st.session_state['page'] == 'predict':
    show_predict()
    if st.button("Back to Home"):
        navigate_to('home')

# Compare page
elif st.session_state['page'] == 'compare':
    compare_teams()  # compare_teams() fonksiyonunu burada çağırın
    if st.button("Back to Home"):
        navigate_to('home')

# CSS to style the app background
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://img1.getimg.ai/generated/img-VocOZEcYGF4mh18aVV52o.jpeg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
