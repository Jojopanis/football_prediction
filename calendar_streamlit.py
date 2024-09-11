import streamlit as st
import os

# Dictionary with team names as keys and logo paths as values
team_names = {
    'Standard': 'Standard',
    'Anderlecht': 'Anderlecht',
    # Add other teams here
}

# Path to the logos
team_logo = {team: f"data/logos/{name.lower().replace(' ', '_')}.png" for team, name in team_names.items()}

# Streamlit layout with columns
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("Home Team", list(team_names.keys()), key='home_team_selector')
    logo_path_home = team_logo[home_team]
    if os.path.isfile(logo_path_home):
        st.image(logo_path_home, width=60, caption=home_team)
    else:
        st.write(f"Logo not found for {home_team}")

with col2:
    away_team = st.selectbox("Away Team", list(team_names.keys()), key='away_team_selector')
    logo_path_away = team_logo[away_team]
    if os.path.isfile(logo_path_away):
        st.image(logo_path_away, width=60, caption=away_team)
    else:
        st.write(f"Logo not found for {away_team}")
