import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import plotly.express as px
import base64

# Load predictions
prediction = pd.read_csv('data/predictions.csv')
prediction = prediction.rename(columns={
    'HomeTeam': 'HomeTeam',
    'AwayTeam': 'AwayTeam',
    'Date': 'Date',
    'FTR_H': 'Home wins',
    'FTR_D': 'Draw',
    'FTR_A': 'Away wins',
    'Prediction': 'Prediction'
})
# Function to determine the prediction label
def get_prediction_label(row):
    # Determine the prediction based on the highest probability
    max_prob = max(row['Home wins'], row['Draw'], row['Away wins'])
    if max_prob == row['Home wins']:
        return f'{row["HomeTeam"]} wins'
    elif max_prob == row['Draw']:
        return 'Draw'
    else:
        return f'{row["AwayTeam"]} wins'

# Apply the prediction label function to the DataFrame
prediction['Prediction'] = prediction.apply(get_prediction_label, axis=1)

logos_folder = "data/logos/"

# Function to switch to the details page with the selected event's prediction
def show_prediction(event_index):
    st.session_state['page'] = 'details'
    st.session_state['selected_event'] = event_index

# Function to get base64-encoded image data
def get_logo_base64(team):
    img_path = f"{logos_folder}{team}.png"
    try:
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return ""


st.markdown(
    """
    <style>
    .stApp {
        background: url("https://img1.getimg.ai/generated/img-oUzQl2VcGvfTvt01afrXN.jpeg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center the image and adjust its size
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column width ratios as needed

with col1:
    st.write("")  # Empty column for spacing
with col2:
    st.image('data\logos\jupilerproleague.png', use_column_width=False, width=300)  # Adjust width to make it bigger
with col3:
    st.write("")  # Empty column for spacing

st.title('🍻 Jupiler Pro League 🍻')

# Page Selection Logic
if 'page' not in st.session_state:
    st.session_state['page'] = 'calendar'  # Default page is the calendar

# Calendar Mode selection
mode = st.selectbox(
    "Calendar Mode:",
    ("daygrid", "list")
)

# Create events from the prediction data
events = []
for idx, row in prediction.iterrows():
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    home_logo = get_logo_base64(home_team)  # Get base64 logo for home team
    away_logo = get_logo_base64(away_team)  # Get base64 logo for away team
    
    # Create event with text
    events.append(
        {
            "title": f"{home_team} vs {away_team}",
            "color": "#FF6C6C",
            "start": row['Date'],
            "end": row['Date'],
            "probabilities": row["Home wins"] + row["Draw"] + row["Away wins"],
            "prediction": row["Prediction"],
            "home_logo": home_logo,
            "away_logo": away_logo,
            "id": int(idx),
        }
    )

# Define calendar options
calendar_options = {
    "initialView": mode,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
    },
}

# Configure view based on mode
if mode == 'list':
    calendar_options = {
        **calendar_options,
        "initialDate": "2024-09-13",
        "initialView": "listMonth",
    }
elif mode == 'daygrid':
    calendar_options = {
        **calendar_options,
        "initialDate": "2024-09-13",
        "initialView": "dayGridMonth",
    }


# Display the calendar or the details based on session state
if st.session_state['page'] == 'calendar':
    # Calendar page
    state = calendar(
        events=st.session_state.get("events", events),
        options=calendar_options,
        custom_css=""" 
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        """,
        key=mode,
    )
    
    # Check if an event was clicked
    if state.get("eventClick"):
        event_id = state["eventClick"]["event"]["id"]
        show_prediction(int(event_id))  # Cast to int to ensure it's an integer

elif st.session_state['page'] == 'details':
    st.title('Match Prediction Details')
    # Display the prediction details for the selected event
    event_idx = st.session_state['selected_event']
    selected_event = prediction.iloc[int(event_idx)]  # Ensure this is an integer

    # Get logos
    home_team = selected_event['HomeTeam']
    away_team = selected_event['AwayTeam']
    home_logo = get_logo_base64(home_team)
    away_logo = get_logo_base64(away_team)

    # Create HTML content
    html_content = f"""
    <div style="display: flex; align-items: center; justify-content: center;">
        <div style="text-align: center; margin-right: 10px;">
            <img src="{home_logo}" style="width: 80px; height: 80px; vertical-align: middle;">
            <div>{home_team}</div>
        </div>
        <div style="text-align: center; margin: 0 20px;">
            <div style="font-size: 40px;">vs</div>
        </div>
        <div style="text-align: center; margin-left: 10px;">
            <img src="{away_logo}" style="width: 80px; height: 80px; vertical-align: middle;">
            <div>{away_team}</div>
        </div>
    </div>
    <div style="margin-top: 20px;">
        <strong>Prediction:</strong> {selected_event['Prediction']}<br>
        <strong>Date:</strong> {selected_event['Date']}<br>
        <strong>Probabilities:</strong> Home wins: {selected_event['Home wins']}, Draw: {selected_event['Draw']}, Away wins: {selected_event['Away wins']}
    </div>
    """

    st.markdown(html_content, unsafe_allow_html=True)

    # Display pie chart
    fig = px.pie(
        values=[selected_event['Home wins'], selected_event['Draw'], selected_event['Away wins']],
        names=['Home wins', 'Draw', 'Away wins'],
        title='Probabilities'
    )
    st.plotly_chart(fig)

    # Back button to return to calendar
    if st.button("Back to Calendar"):
        st.session_state['page'] = 'calendar'
