# NBA Players Stats Explorer Application

import pandas as pd
import streamlit as st
import base64
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np

# Application title
st.title("NBA Players Stats Explorer")

# Brief information about the application
st.markdown('''
This application performs web scraping of NBA player stats data!

* ***Python Libraries:*** pandas, base64, streamlit
* ***Data Source:*** [basketball-reference.com](https://www.basketball-reference.com/)
''')

# Sidebar header
st.sidebar.header("User Input Features")

# Selectbox for different years
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950,2020))))

# Function to load data of different years to the application
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    new_df = df.drop(df[df.Age == 'Age'].index)
    new_df = new_df.fillna(0)
    playerstats = new_df.drop(['Rk'], axis=1)
    
    return playerstats

playerstats = load_data(selected_year)

# Team select box
sorted_teams = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect("Teams", sorted_teams, sorted_teams)

# Position select box
positions = sorted(playerstats.Pos.unique())
selected_positions = st.sidebar.multiselect("Positions", positions, positions)

# New data base on selected team(s) and position(s)
df_selected = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_positions))]

# DataFrame header
st.header("Display Players Stats Based on Selected Team(s) and Position(s)")

# Information about selected teams
team_list = sorted(list(df_selected.Tm.unique()))
team_list_to_string = ', '.join([str(team) for team in team_list])
st.write("***Selected Teams:***" + " " + team_list_to_string)

# Information about selected positions
pos_list = sorted(list(df_selected.Pos.unique()))
pos_list_to_string = ', '.join([str(pos) for pos in pos_list])
st.write("***Selected Positions:***" + " " + pos_list_to_string)

# DataFrame
st.dataframe(df_selected)
st.write("Data: " + str(df_selected.shape[0]) + " rows and " + str(df_selected.shape[1]) + " columns")

# Download data as csv file
def csv_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # for string - byte conversion
    href = f'<a href="data:file/csv;base64,{b64}" download = "nba_playerstats.csv">Download csv file</a>'
    return href

st.markdown(csv_download(df_selected), unsafe_allow_html=True)
