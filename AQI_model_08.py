#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import folium
from streamlit_folium import folium_static

# Load data from your specific file path
data_file = r'C:/Users/HP/watch/AQI_fill.csv'

# Streamlit app layout
st.title("AQI Monitoring Tool")

# Create columns for logos
col1, col2, col3, col4, col5 = st.columns(5)

# Add logos in each column
with col1:
    st.image(r'C:/Users/HP/watch/nitw.png', width=100)  # NIT Warangal logo
with col2:
    st.image(r'C:/Users/HP/watch/cuny.png', width=100)  # CUNY logo
with col3:
    st.image(r'C:/Users/HP/watch/kiss.png', width=100)  # KISS logo
with col4:
    st.image(r'C:/Users/HP/watch/usindia.png', width=100)  # US-India logo
with col5:
    st.image(r'C:/Users/HP/watch/watch.png', width=100)  # Watch logo

st.write("---")  # Adds a horizontal line for separation

# Map Feature for NIT Warangal
latitude = 17.9836  # Latitude for NIT Warangal
longitude = 79.5308  # Longitude for NIT Warangal

# Create a map centered around NIT Warangal
m = folium.Map(location=[latitude, longitude], zoom_start=15)

# Add a marker for the monitoring station
folium.Marker([latitude, longitude], tooltip='NIT Warangal Monitoring Station').add_to(m)

# Display the map in the Streamlit app
st.write("### AQI Monitoring Stations NIT Warangal")
folium_static(m)

# Read the file using the correct delimiter (comma)
data = pd.read_csv(data_file, delimiter=',')  # Ensure delimiter is correct
data.columns = data.columns.str.strip()  # Clean column names

# Display the first few rows and column names for debugging
st.write("### Data Preview")
st.write(data.head())
st.write("Columns:", data.columns.tolist())

# Check if 'timestamp', 'AQIH', 'PM2.5', and 'PM10' exist in the columns
required_columns = ['timestamp', 'AQIH', 'PM2.5', 'PM10']
if not all(col in data.columns for col in required_columns):
    st.error("Required columns 'timestamp', 'AQIH', 'PM2.5', or 'PM10' not found in the data.")
else:
    # Parse dates
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%d-%m-%Y %H:%M', dayfirst=True)

    # Function to calculate statistics
    def calculate_statistics(df):
        return {
            'Average AQI': df['AQIH'].mean(),
            'Max AQI': df['AQIH'].max(),
            'Min AQI': df['AQIH'].min(),
            'Average PM2.5': df['PM2.5'].mean(),
            'Max PM2.5': df['PM2.5'].max(),
            'Min PM2.5': df['PM2.5'].min(),
            'Average PM10': df['PM10'].mean(),
            'Max PM10': df['PM10'].max(),
            'Min PM10': df['PM10'].min(),
        }

    # Function to plot AQI over time
    def plot_aqi(df):
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df['AQIH'], marker='o', label='AQI (15 min intervals)', color='blue')
        plt.title('AQI Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('AQI')
        plt.xticks(rotation=45)

        # Adding horizontal lines for AQI thresholds with different colors
        plt.axhline(y=50, color='blue', linestyle='--', label='AQI 50 (Good)')
        plt.axhline(y=100, color='yellow', linestyle='--', label='AQI 100 (Moderate)')
        plt.axhline(y=150, color='orange', linestyle='--', label='AQI 150 (Unhealthy for Sensitive Groups)')
        plt.axhline(y=200, color='red', linestyle='--', label='AQI 200 (Unhealthy)')

        plt.legend()
        plt.tight_layout()
        st.pyplot(plt)

    # Function to plot PM2.5 over time
    def plot_pm25(df):
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df['PM2.5'], marker='o', label='PM2.5', color='orange')
        plt.title('PM2.5 Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('PM2.5 Concentration (µg/m³)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

    # Function to plot PM10 over time
    def plot_pm10(df):
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df['PM10'], marker='o', label='PM10', color='green')
        plt.title('PM10 Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('PM10 Concentration (µg/m³)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

    # Function to analyze hourly averages and suggest general no-go times
    def analyze_hourly_aqi(df):
        df.set_index('timestamp', inplace=True)
        hourly_avg = df.resample('H').mean()
        high_aqi_times = hourly_avg[hourly_avg['AQIH'] > 150]

        return high_aqi_times.index.hour.value_counts().sort_index()

    # Function to plot high AQI counts
    def plot_high_aqi_counts(high_aqi_counts):
        plt.figure(figsize=(12, 6))
        high_aqi_counts.plot(kind='bar', color='red')
        plt.title('Hourly High AQI Counts')
        plt.xlabel('Hour of Day')
        plt.ylabel('Count of High AQI Readings')
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(plt)

    # Health tips based on AQI levels
    def health_tips(aqi):
        if aqi <= 50:
            return "Air quality is satisfactory; air pollution poses little or no risk."
        elif aqi <= 100:
            return "Air quality is acceptable; however, some pollutants may be a concern for a small number of people."
        elif aqi <= 150:
            return "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
        elif aqi <= 200:
            return "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
        elif aqi <= 300:
            return "Health alert: everyone may experience more serious health effects."
        else:
            return "Health warnings of emergency conditions. The entire population is more likely to be affected."

    # AQI Statistics Section
    st.write("### AQI Statistics")
    stats = calculate_statistics(data)
    for key, value in stats.items():
        st.write(f"{key}: {value}")

    st.write("### AQI Over Time (15 Min Intervals)")
    plot_aqi(data)

    st.write("### PM2.5 Over Time (15 Min Intervals)")
    plot_pm25(data)

    st.write("### PM10 Over Time (15 Min Intervals)")
    plot_pm10(data)

    # Analyze and plot high AQI counts
    high_aqi_counts = analyze_hourly_aqi(data)
    if not high_aqi_counts.empty:
        plot_high_aqi_counts(high_aqi_counts)
    else:
        st.write("Air quality is generally safe throughout the day.")

    # Health Tips Section
    st.write("### Health Tips Based on AQI Levels")
    aqi_value = st.number_input("Enter an AQI value to get health tips:", min_value=0, value=0)
    if aqi_value is not None:
        st.write(health_tips(aqi_value))


# In[ ]:




