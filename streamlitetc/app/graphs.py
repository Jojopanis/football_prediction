import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_graphs():
    st.title("Football Match Statistics")

    df = pd.read_csv("standing.csv")

    tab1, tab2 = st.tabs(["Statistics", "Team Standings"])

    df2 = df.groupby('HomeTeam').mean().reset_index()
    df2['Average_Points_Per_Match'] = df2['Points'] / df2['Matches_Played']
    df2['Average_Goals_For_Per_Match'] = df2['Goals_For'] / df2['Matches_Played']
    df2['Average_Goals_Against_Per_Match'] = df2['Goals_Against'] / df2['Matches_Played']
    df2['Average_Goal_Difference_Per_Match'] = df2['Goal_Difference'] / df2['Matches_Played']

    with tab1:
        st.subheader("Select the statistic to view:")
        stat_tab1, stat_tab2, stat_tab3, stat_tab4, stat_tab5, stat_tab6 = st.tabs([
            "Average Points Per Match",
            "Average Goals Per Match",
            "Average Goals Against Per Match",
            "Goals For vs Goals Against",
            "Points vs Matches Played",
            "Team Performance Overview"
        ])

        with stat_tab1:
            fig = px.bar(df2, x='HomeTeam', y='Average_Points_Per_Match',
                         title='Average Points Per Match by Team',
                         labels={'HomeTeam': 'Team', 'Average_Points_Per_Match': 'Average Points Per Match'},
                         color='Average_Points_Per_Match', color_continuous_scale='Blues')
            st.plotly_chart(fig)

        with stat_tab2:
            fig = px.bar(df2, x='HomeTeam', y='Average_Goals_For_Per_Match',
                         title='Average Goals For Per Match by Team',
                         labels={'HomeTeam': 'Team', 'Average_Goals_For_Per_Match': 'Average Goals For Per Match'},
                         color='Average_Goals_For_Per_Match', color_continuous_scale='Greens')
            st.plotly_chart(fig)

        with stat_tab3:
            fig = px.bar(df2, x='HomeTeam', y='Average_Goals_Against_Per_Match',
                         title='Average Goals Against Per Match by Team',
                         labels={'HomeTeam': 'Team', 'Average_Goals_Against_Per_Match': 'Average Goals Against Per Match'},
                         color='Average_Goals_Against_Per_Match', color_continuous_scale='Reds')
            st.plotly_chart(fig)

        with stat_tab4:
            fig = px.scatter(df2, x='Average_Goals_For_Per_Match', y='Average_Goals_Against_Per_Match',
                             color='HomeTeam', size='Average_Goals_For_Per_Match',
                             title='Goals For vs Goals Against',
                             labels={'Average_Goals_For_Per_Match': 'Average Goals For Per Match',
                                     'Average_Goals_Against_Per_Match': 'Average Goals Against Per Match'},
                             hover_name='HomeTeam', color_continuous_scale='Viridis')
            st.plotly_chart(fig)

        with stat_tab5:
            fig = px.scatter(df2, x='Matches_Played', y='Points',
                             color='HomeTeam', size='Points',
                             title='Points vs Matches Played',
                             labels={'Matches_Played': 'Matches Played', 'Points': 'Points'},
                             hover_name='HomeTeam', color_continuous_scale='Cividis')
            st.plotly_chart(fig)

        with stat_tab6:
            fig = px.line(df2, x='HomeTeam', y=['Average_Goals_For_Per_Match', 'Average_Goals_Against_Per_Match', 'Average_Points_Per_Match'],
                          labels={'value': 'Average Metrics', 'variable': 'Metric'},
                          title='Team Performance Overview')
            st.plotly_chart(fig)

    with tab2:
        st.subheader("Team Standings")

        standings_df = df[['HomeTeam', 'Points', 'Matches_Played', 'Goals_For', 'Goals_Against', 'Goal_Difference']]
        standings_df = standings_df.sort_values(by='Points', ascending=False)

        st.write("**Current Team Standings:**")
        st.table(standings_df)


    