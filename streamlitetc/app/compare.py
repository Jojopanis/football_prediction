import streamlit as st
import pandas as pd
import plotly.express as px

def compare_teams():
    st.title("Football Team Comparison")

    df = pd.read_csv("standing.csv")

    st.header("Compare Two Teams")

    teams = df['HomeTeam'].unique()

    team1 = st.selectbox("Select the first team:", teams)
    team2 = st.selectbox("Select the second team:", teams)

    if team1 and team2:
        team1_data = df[df['HomeTeam'] == team1]
        team2_data = df[df['HomeTeam'] == team2]

        team1_stats = {
            'Matches Played': team1_data['Matches_Played'].sum(),
            'Points': team1_data['Points'].sum(),
            'Goals For': team1_data['Goals_For'].sum(),
            'Goals Against': team1_data['Goals_Against'].sum(),
            'Goal Difference': team1_data['Goal_Difference'].sum()
        }

        team2_stats = {
            'Matches Played': team2_data['Matches_Played'].sum(),
            'Points': team2_data['Points'].sum(),
            'Goals For': team2_data['Goals_For'].sum(),
            'Goals Against': team2_data['Goals_Against'].sum(),
            'Goal Difference': team2_data['Goal_Difference'].sum()
        }

        st.subheader(f"Statistics for {team1} vs {team2}")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{team1} Statistics:**")
            for stat, value in team1_stats.items():
                st.write(f"{stat}: {value}")

        with col2:
            st.write(f"**{team2} Statistics:**")
            for stat, value in team2_stats.items():
                st.write(f"{stat}: {value}")

        comparison_df = pd.DataFrame({
            'Statistic': ['Matches Played', 'Points', 'Goals For', 'Goals Against', 'Goal Difference'],
            team1: list(team1_stats.values()),
            team2: list(team2_stats.values())
        })

        fig = px.bar(comparison_df, x='Statistic', y=[team1, team2],
                     barmode='group', title=f'Comparison between {team1} and {team2}')
        st.plotly_chart(fig)

        st.subheader("Head-to-Head Performance")
        head_to_head = df[(df['HomeTeam'].isin([team1, team2])) & (df['HomeTeam'].isin([team1, team2]))]
        st.write(head_to_head[['HomeTeam', 'Goals_For', 'Goals_Against', 'Points']])
        
        team1_wins = len(head_to_head[(head_to_head['HomeTeam'] == team1) & (head_to_head['Points'] == 3)]) + \
                     len(head_to_head[(head_to_head['HomeTeam'] == team1) & (head_to_head['Points'] == 0)])
        team2_wins = len(head_to_head[(head_to_head['HomeTeam'] == team2) & (head_to_head['Points'] == 3)]) + \
                     len(head_to_head[(head_to_head['HomeTeam'] == team2) & (head_to_head['Points'] == 0)])
        draws = len(head_to_head) - team1_wins - team2_wins
        
        st.write(f"**{team1} Wins:** {team1_wins}")
        st.write(f"**{team2} Wins:** {team2_wins}")
        st.write(f"**Draws:** {draws}")
