#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:18:28 2024

@author: hugoramos
"""
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import plotly.express as px

# Load the datasets
global_data = pd.read_excel('Global_data.xlsx')
physical_data = pd.read_excel('Physical_data.xlsx')
after_game_data = pd.read_excel('After_Game_data.xlsx')

# Clean the names by stripping whitespace and converting to lowercase
def clean_names(df):
    df['First Name'] = df['First Name'].str.strip().str.lower()
    df['Last Name'] = df['Last Name'].str.strip().str.lower()
    return df

global_data = clean_names(global_data)
physical_data = clean_names(physical_data)
after_game_data = clean_names(after_game_data)

# Merge datasets on 'First Name' and 'Last Name' using outer merge to include all athletes
merged_data = global_data.merge(physical_data, on=['First Name', 'Last Name'], how='outer').merge(after_game_data, on=['First Name', 'Last Name'], how='outer')

# Remove entries where all relevant data is missing
merged_data = merged_data.dropna(subset=['Age', 'Height(cm)', 'Weight(kg)', 'Foot', 'Position', 'Date of the game', 'Game Results'], how='all')

# Combine first and last names for selection
merged_data['full_name'] = merged_data['First Name'].str.capitalize() + ' ' + merged_data['Last Name'].str.capitalize()

# Streamlit app
st.set_page_config(layout="wide")  # Extend page size

# Custom CSS styles for better layout and fonts
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content .css-1v3fvcr {
        padding-top: 1rem;
    }
    .title-font {
        font-family: 'Georgia', serif;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
    }
    .section-title {
        font-family: 'Georgia', serif;
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subsection-title {
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #34495e;
    }
    .sidebar .sidebar-content .css-1lcbmhc {
        margin-top: 0.5rem;
    }
    .insight-button {
        background-color: #3498db;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

logo = Image.open('ubuntu_logo.webp')
logo = logo.resize((100, 100))
st.sidebar.image(logo, use_column_width=True)
st.sidebar.title("Ubuntu Pro Sports Dashboard")

athlete_name = st.sidebar.selectbox('Select an athlete:', [''] + list(merged_data['full_name'].unique()))

if not athlete_name:
    # Home page content centered
    st.markdown("""
        <div style="display: flex; height: 100vh; align-items: center; justify-content: center; text-align: center;">
            <div>
                <h1 class="title-font">Welcome to Ubuntu Athlete Performance Analysis</h1>
                <h2 class="section-title">About This Dashboard</h2>
                <p>This dashboard provides detailed analysis and evolution of athletes based on their physical performances. 
                You can select an athlete from the sidebar to view their profile, physical condition, recent game performances, and key takeaways.
                The dashboard helps in tracking the progress and performance of athletes to ensure they are on the right path to achieving their goals.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Athlete's profile page content
    athlete_data = merged_data[merged_data['full_name'] == athlete_name].copy()
    
    # Convert 'Date of the game' to datetime
    athlete_data['Date'] = pd.to_datetime(athlete_data['Date of the game'], errors='coerce')

    # Get athlete's first and last name for loading the photo
    first_name = athlete_data['First Name'].iloc[0].capitalize()
    last_name = athlete_data['Last Name'].iloc[0].capitalize()
    
    # Dynamic title for each player
    st.markdown(f"<h1 class='title-font'>{first_name} {last_name} Performance Overview</h1>", unsafe_allow_html=True)
    
    # Construct the photo filename
    if first_name == 'Hugo':
        photo_filename = "Hugo_profile_photo.jpeg"
    elif first_name == 'Uday':
        photo_filename = "Uday_profile_photo.jpeg"
    elif first_name == 'Emanuele':
        photo_filename = "Emanuele_profile_photo.jpeg"
    else:
        photo_filename = None
    
    col1, col2 = st.columns([1, 3])  # Adjust column width to make space for the image and player info together
    
    with col1:
        # Display the profile photo
        if photo_filename:
            try:
                img = Image.open(photo_filename)
                st.image(img, caption=f"{first_name} {last_name}", use_column_width=True)
            except FileNotFoundError:
                st.write("Profile photo not available.")
    
    with col2:
        # Player Info and Physical Condition in the same column
        st.markdown("""
            <div style="display: flex; flex-direction: column;">
                <div style="margin-bottom: 20px;">
                    <h2 class='subsection-title'>Player Info</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Age:</strong> {age}</p>
                    <p><strong>Height:</strong> {height} cm</p>
                    <p><strong>Weight:</strong> {weight} kg</p>
                    <p><strong>Foot:</strong> {foot}</p>
                    <p><strong>Position:</strong> {position}</p>
                </div>
                <div>
                    <h2 class='subsection-title'>Physical Condition</h2>
                    <p><strong>Monthly Average Exertion Training:</strong> {exertion_training:.2f}</p>
                    <p><strong>Monthly Average Exertion Game:</strong> {exertion_game:.2f}</p>
                    <p><strong>Monthly Average 30m Sprint time:</strong> {sprint_time:.2f} seconds</p>
                    <p><strong>Monthly Average Sleep Quality:</strong> {sleep_quality:.2f}</p>
                    <p><strong>Monthly Average Flexibility:</strong> {flexibility:.2f} cm</p>
                    <p><strong>Monthly Average Jump:</strong> {jump:.2f} cm</p>
                </div>
            </div>
        """.format(
            name=f"{first_name} {last_name}",
            age=athlete_data['Age'].iloc[0],
            height=athlete_data['Height(cm)'].iloc[0],
            weight=athlete_data['Weight(kg)'].iloc[0],
            foot=athlete_data['Foot'].iloc[0],
            position=athlete_data['Position'].iloc[0],
            exertion_training=athlete_data['Exertion Training'].mean(),
            exertion_game=athlete_data['Exertion Games'].mean(),
            sprint_time=athlete_data['30m Sprint time (seconds)'].mean(),
            sleep_quality=athlete_data['Sleep Quality'].mean(),
            flexibility=athlete_data['Flexibility (cm)'].mean(),
            jump=athlete_data['Vertical Jump (in cm)'].mean()
        ), unsafe_allow_html=True)
    
    # Most Recent 5 Game Performance
    st.markdown("<h2 class='section-title'>Most Recent 5 Game Performance</h2>", unsafe_allow_html=True)
    if not athlete_data['Date'].isnull().all():
        recent_games = athlete_data.sort_values(by='Date', ascending=False).head(5)
        recent_games_table = recent_games[['Date of the game', 'Time played(min)', 'Game Results', 'Goals Scored', 'Assist', 'Fouls Commited', 'Numbers of Times Fouled']]
        recent_games_table.columns = ['Date', 'Minutes Played', 'Result', 'Goals Scored', 'Assists', 'Fouls Committed', 'Fouls Received']
        st.table(recent_games_table)
    else:
        st.write("No game performance data available.")
    
        # Key Takeaways
    st.markdown("<h2 class='section-title'>Key Takeaways</h2>", unsafe_allow_html=True)
    
    if not athlete_data['Date'].isnull().all():
        overall_satisfaction = recent_games['Overall Feeling'].mean() * 100
        physical_satisfaction = recent_games['Physical Feeling'].mean() * 100
    
        col3, col4 = st.columns([1, 1], gap="large")  # Increase the gap between the columns
    
        with col3:
            fig1 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_satisfaction,
                title={'text': "Overall Average Satisfaction"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': overall_satisfaction}}))
            fig1.update_layout(height=300)
            st.plotly_chart(fig1)
    
        with col4:
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=physical_satisfaction,
                title={'text': "Physical Average Satisfaction"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': physical_satisfaction}}))
            fig2.update_layout(height=300)
            st.plotly_chart(fig2)
    else:
        st.write("No satisfaction data available.")
    
    st.markdown("<h2 class='section-title'>Key Insights</h2>", unsafe_allow_html=True)
    
    if st.button('Find out key insights', key='insights_button'):
        insights = []
        if overall_satisfaction < 60:
            insights.append("The player's overall game feeling is below 60%. Focus on improving game strategies and providing additional support.")
    
        if physical_satisfaction < 60:
            insights.append("The player's physical feeling is below 60%. Pay attention to their physical training and recovery routines.")
    
        # Check for recent injuries
        if 'Injuries' in athlete_data.columns:
            recent_injuries = athlete_data[athlete_data['Injuries'].notnull()]
            if not recent_injuries.empty:
                for injury in recent_injuries['Injuries'].unique():
                    if 'Major' in injury:
                        insights.append(f"Recent injury recorded: Major - {injury}. Ensure proper medical attention and recovery plans are in place.")
                    elif 'Minor' in injury:
                        insights.append(f"Recent injury recorded: Minor - {injury}. Ensure proper medical attention and recovery plans are in place.")
    
        if insights:
            for insight in insights:
                st.write("- " + insight)
        else:
            st.write("The player is in great shape!!")
    
    col5, col6 = st.columns(2)
    
    with col5:
        # Monthly Average Exertion Levels (Training vs. Game)
        if not athlete_data['Date'].isnull().all():
            numeric_cols = ['Exertion Training', 'Exertion Games']
            athlete_data[numeric_cols] = athlete_data[numeric_cols].apply(pd.to_numeric, errors='coerce')
            monthly_avg = athlete_data.resample('M', on='Date')[numeric_cols].mean()
            st.write("Monthly average exertion levels (Training vs. Game) - debug:")
            st.write(monthly_avg)
            
            fig_exertion = px.bar(
                athlete_data,
                x='Date',
                y=numeric_cols,
                labels={'value': 'Exertion Level', 'Date': 'Date'},
                title='Exertion Levels (Training vs. Game)',
                barmode='group'
            )
            st.plotly_chart(fig_exertion)
        else:
            st.write("No exertion data available.")
    
    with col6:
        # Monthly Average Sleep Quality
        if not athlete_data['Date'].isnull().all():
            athlete_data['Sleep Quality'] = pd.to_numeric(athlete_data['Sleep Quality'], errors='coerce')
            monthly_avg = athlete_data.resample('M', on='Date')['Sleep Quality'].mean()
            st.write("Monthly average sleep quality - debug:")
            st.write(monthly_avg)
            
            fig_sleep = px.bar(
                athlete_data,
                x='Date',
                y='Sleep Quality',
                labels={'Sleep Quality': 'Sleep Quality', 'Date': 'Date'},
                title='Sleep Quality Over Time'
            )
            st.plotly_chart(fig_sleep)
        else:
            st.write("No sleep quality data available.")


        
        