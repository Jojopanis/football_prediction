import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

# Load predictions
prediction = pd.read_csv('data/predictions.csv')

logos_folder = "data/logos/"
# Page Selection Logic
if 'page' not in st.session_state:
    st.session_state['page'] = 'calendar'  # Default page is the calendar

# Function to switch to the details page with the selected event's prediction
def show_prediction(event_index):
    st.session_state['page'] = 'details'
    st.session_state['selected_event'] = event_index

# Calendar Mode selection
mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "list"
    ),
)



def get_logo(team):
    return f"{logos_folder}{team}.png"
# Create events from the prediction data
events = []
for idx, row in prediction.iterrows():
    # Get team names and their logos
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    home_logo = get_logo(home_team)  # Get local logo path
    away_logo = get_logo(away_team)  # Get local logo path

    if home_logo:
        home_logo_html = f'<img src="{home_logo}" style="width:16px; height:16px; vertical-align:middle;">'
    else:
        home_logo_html = ''
    if away_logo:
        away_logo_html = f'<img src="{away_logo}" style="width:16px; height:16px; vertical-align:middle;">'
    else:
        away_logo_html = ''

    # Construct event title with team names and logos
    title_with_logos = f"""
        {home_logo_html} {home_team}
        vs
        {away_logo_html} {away_team}
    """

    # Append the event to the list
    events.append(
        {
            "title": title_with_logos,  # Set the title with logos
            "color": "#FF6C6C",
            "start": row['Date'],
            "end": row['Date'],
            "probabilities": row["FTR_A"] + row["FTR_D"] + row["FTR_H"],
            "prediction": row["Prediction"],
            "id": int(idx),  # Ensure ID is an integer
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
    # Display the prediction details for the selected event
    event_idx = st.session_state['selected_event']
    selected_event = prediction.iloc[int(event_idx)]  # Ensure this is an integer

    st.write(f"### Match: {selected_event['HomeTeam']} vs {selected_event['AwayTeam']}")
    st.write(f"**Prediction**: {selected_event['Prediction']}")
    st.write(f"**Date**: {selected_event['Date']}")
    st.write(f"**Probabilities**: Home: {selected_event['FTR_H']}, Draw: {selected_event['FTR_D']}, Away: {selected_event['FTR_A']}")

    # Back button to return to calendar
    if st.button("Back to Calendar"):
        st.session_state['page'] = 'calendar'
