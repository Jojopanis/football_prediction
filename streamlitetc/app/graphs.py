import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_graphs():
    st.title("Football Match Statistics")

    df = pd.read_csv("standing.csv")

    st.header("Graphs")


    tab1, tab2 = st.tabs(["Team Statistics", "Standings",])

    with tab1:
        
        
        st.subheader("Team Statistics")
        
        df2 = df.groupby('HomeTeam').mean().reset_index()
        df2['Average_Points_Per_Match'] = df2['Points'] / df2['Matches_Played']
        df2['Average_Goals_For_Per_Match'] = df2['Goals_For'] / df2['Matches_Played']
        df2['Average_Goals_Against_Per_Match'] = df2['Goals_Against'] / df2['Matches_Played']
        df2['Average_Goal_Difference_Per_Match'] = df2['Goal_Difference'] / df2['Matches_Played']
        

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        axes[0, 0].barh(df2['HomeTeam'], df2['Average_Points_Per_Match'], color='skyblue')
        axes[0, 0].set_xlabel('Average Points Per Match')
        axes[0, 0].set_title('Average Points Per Match by Team')

        axes[0, 1].barh(df2['HomeTeam'], df2['Average_Goals_For_Per_Match'], color='lightgreen')
        axes[0, 1].set_xlabel('Average Goals For Per Match')
        axes[0, 1].set_title('Average Goals For Per Match by Team')

        axes[1, 0].barh(df2['HomeTeam'], df2['Average_Goals_Against_Per_Match'], color='salmon')
        axes[1, 0].set_xlabel('Average Goals Against Per Match')
        axes[1, 0].set_title('Average Goals Against Per Match by Team')

        axes[1, 1].barh(df2['HomeTeam'], df2['Average_Goal_Difference_Per_Match'], color='lightcoral')
        axes[1, 1].set_xlabel('Average Goal Difference Per Match')
        axes[1, 1].set_title('Average Goal Difference Per Match by Team')

        plt.tight_layout()
        st.pyplot(fig)


    with tab2:
        
        st.subheader("Team Standings")
        st.write(df.sort_values('Points', ascending=False))
        
