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

# Load championship leaderboard
championship_leaders = pd.read_csv('data/championship_leaders.csv')
championship_leaders.reset_index(inplace=True)

# Function to determine the prediction label
def get_prediction_label(row):
    max_prob = max(row['Home wins'], row['Draw'], row['Away wins'])
    if max_prob == row['Home wins']:
        return f'{row["HomeTeam"]} wins'
    elif max_prob == row['Draw']:
        return 'Draw'
    else:
        return f'{row["AwayTeam"]} wins'

# Function to calculate the odds based on the probabilities
def calculate_odds(probability):
    if probability > 0:
        return round(1 / probability * 100, 2)  # Round to 2 decimal places
    else:
        return float('inf')  # Handle cases where probability is zero

# Apply the prediction label function to the DataFrame
prediction['Prediction'] = prediction.apply(get_prediction_label, axis=1)

# Calculate odds for each outcome
prediction['Odds_HomeWins'] = prediction['Home wins'].apply(calculate_odds)
prediction['Odds_Draw'] = prediction['Draw'].apply(calculate_odds)
prediction['Odds_AwayWins'] = prediction['Away wins'].apply(calculate_odds)

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
        background: url("https://img1.getimg.ai/generated/img-VocOZEcYGF4mh18aVV52o.jpeg");
        background-size: cover;
    }
    .title-center {
        text-align: center;
        font-size: 30px;
    }
    .sub-title-center {
        text-align: center;
        font-size: 24px;
    }
    .team-column {
        text-align: center;
        font-size: 20px;
    }
    .logo {
        width: 80px;
        height: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with radio button to switch between Calendar and Leaderboard
page_selection = st.sidebar.radio(
    "Navigation",
    ("Home (Calendar)", "Championship Leaderboard")
)

# Center the main title
st.markdown('<h1 class="title-center">🍻 Jupiler Pro League 🍻</h1>', unsafe_allow_html=True)

# Calendar or Leaderboard based on selection
if page_selection == "Home (Calendar)":

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
    if 'page' not in st.session_state:
        st.session_state['page'] = 'calendar'  # Default page is the calendar

    if st.session_state['page'] == 'calendar':
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
        st.markdown('<h2 class="sub-title-center">Match Prediction Details</h2>', unsafe_allow_html=True)
        
        # Display the prediction details for the selected event
        event_idx = st.session_state['selected_event']
        selected_event = prediction.iloc[int(event_idx)]  # Ensure this is an integer

        # Get logos
        home_team = selected_event['HomeTeam']
        away_team = selected_event['AwayTeam']
        home_logo = get_logo_base64(home_team)
        away_logo = get_logo_base64(away_team)

        # Team logos and names centered
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; margin-right: 10px;">
                <img src="{home_logo}" class="logo">
                <div>{home_team}</div>
            </div>
            <div style="text-align: center; margin: 0 20px;">
                <div style="font-size: 40px;">vs</div>
            </div>
            <div style="text-align: center; margin-left: 10px;">
                <img src="{away_logo}" class="logo">
                <div>{away_team}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Centered Prediction and Date on top
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <strong>Prediction:</strong> {selected_event['Prediction']}<br>
            <strong>Date:</strong> {selected_event['Date']}<br>
        </div>
        """, unsafe_allow_html=True)

        # Odds and Probabilities below in two columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### Probabilities")
            st.write(f"**Home wins**: {selected_event['Home wins']}")
            st.write(f"**Draw**: {selected_event['Draw']}")
            st.write(f"**Away wins**: {selected_event['Away wins']}")

        with col2:
            st.markdown(f"### Odds")
            st.write(f"**Home wins**: {selected_event['Odds_HomeWins']}")
            st.write(f"**Draw**: {selected_event['Odds_Draw']}")
            st.write(f"**Away wins**: {selected_event['Odds_AwayWins']}")

        custom_colors = ["#7CC674", "#73C5C5", "#C9190B"]
        # Display pie chart for probabilities
        fig = px.pie(
            values=[selected_event['Home wins'], selected_event['Draw'], selected_event['Away wins']],
            names=['Home wins', 'Draw', 'Away wins'],
            title='Probabilities',
            color_discrete_sequence=custom_colors
        )
        st.plotly_chart(fig)

        # Back button to return to calendar
        if st.button("Back to Calendar"):
            st.session_state['page'] = 'calendar'

# Championship Leaderboard Page
# Championship Leaderboard Page
elif page_selection == "Championship Leaderboard":

    st.markdown('<h2 class="sub-title-center">Predicted Championship Leaderboard</h2>', unsafe_allow_html=True)
    
    # Sort championship_leaders by Points in descending order
    championship_leaders.sort_values(by='Points', ascending=False, inplace=True)
    
    # Function to get base64-encoded image data for logos
    def get_logo_base64(team):
        img_path = f"{logos_folder}{team}.png"
        try:
            with open(img_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
        except FileNotFoundError:
            return ""
    
    # Display top 3 teams from championship_leaders.csv with logos
    podium_positions = ["🥇 1st", "🥈 2nd", "🥉 3rd"]
    
    for i in range(3):
        team = championship_leaders.iloc[i]['HomeTeam']
        points = championship_leaders.iloc[i]['Points']
        logo = get_logo_base64(team)
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <div style="flex: 0 0 50px; text-align: center; font-size: 24px; margin-right: 10px;">
                {podium_positions[i]}
            </div>
            <img src="{logo}" class="logo" style="margin-right: 10px;">
            <div style="text-align: left;">
                <div style="font-size: 20px; font-weight: bold;">{team}</div>
                <div style="font-size: 18px;">{points} points</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
