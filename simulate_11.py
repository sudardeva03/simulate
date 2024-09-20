#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Create columns for logos at the top of the interface
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.image(r'C:/Users/HP/watch/nitw.png', width=100)  # NIT Warangal logo
with col2:
    st.image(r'C:/Users/HP/watch/cuny.png', width=100)  # CUNY logo
with col3:
    st.image(r'C:/Users/HP/watch/bronx.png', width=100)  # CUNY logo   
with col4:
    st.image(r'C:/Users/HP/watch/kiss.png', width=100)  # KISS logo
with col5:
    st.image(r'C:/Users/HP/watch/usindia.png', width=100)  # US-India logo
with col6:
    st.image(r'C:/Users/HP/watch/watch.png', width=100)  # Watch logo

# Title of the app
st.title("Campus Air WATCH")

# Recommendations for a Sustainable Campus
st.subheader("Recommendations for a Sustainable Campus")
st.markdown("""
- **Green Building Design**: Use energy-efficient materials and technologies.
- **Renewable Energy Sources**: Install solar panels.
- **Sustainable Transportation**: Promote cycling, walking, and provide EV charging stations.
- **Water Conservation**: Implement rainwater harvesting and drought-resistant landscaping.
- **Waste Reduction and Recycling**: Establish recycling and composting programs.
- **Green Spaces**: Create community gardens and maintain biodiversity.
- **Sustainable Food Options**: Offer locally sourced and organic food.
- **Education and Awareness**: Incorporate sustainability into the curriculum.
- **Community Engagement**: Involve students and staff in sustainability initiatives.
- **Smart Campus Technologies**: Use technology for efficient energy management.
""")

# Load the data from the specified CSV file
file_path = 'C:/Users/HP/watch/AQI_fill.csv'
df = pd.read_csv(file_path)

# Convert the timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')

# Validate data
required_columns = ['AQIH', 'PM2.5', 'PM10']
for column in required_columns:
    if column not in df.columns:
        st.error(f"Column {column} is missing from the data.")
        st.stop()

# Current conditions
current_vegetation_ratio = 0.30  # 25%
current_builtup_ratio = 0.50      # 55%
current_ev_adoption_ratio = 0.05   # 5% EV Adoption

def simulate_aqi(df, vegetation_ratio, ev_adoption_ratio, smog_filter_effectiveness):
    vegetation_effect = 1 - vegetation_ratio
    ev_effect = 1 - ev_adoption_ratio
    filter_effect = 1 - smog_filter_effectiveness
    
    df['AQI_Adjusted'] = df['AQIH'] * vegetation_effect * ev_effect * filter_effect
    df['PM2.5_Adjusted'] = df['PM2.5'] * vegetation_effect * ev_effect * filter_effect
    df['PM10_Adjusted'] = df['PM10'] * vegetation_effect * ev_effect * filter_effect
    
    return df

# Streamlit app layout
st.sidebar.header("Input Parameters")

# Display current conditions
st.sidebar.subheader("Current Conditions")
st.sidebar.write(f"Vegetation Cover: {current_vegetation_ratio * 100:.1f}%")
st.sidebar.write(f"Built-Up Area: {current_builtup_ratio * 100:.1f}%")
st.sidebar.write(f"EV Adoption Rate: {current_ev_adoption_ratio * 100:.1f}%")

# User input for proportions with pre-filled values
vegetation_ratio = st.sidebar.selectbox("Increasing the proportion of Vegetation (%)", 
                                         [i / 100.0 for i in range(10, 101, 5)], 
                                         index=int(current_vegetation_ratio * 20) - 1)
ev_adoption_ratio = st.sidebar.selectbox("Proportion of EV Adoption (%)", 
                                          [i / 100.0 for i in range(10, 101, 5)], 
                                          index=int(current_ev_adoption_ratio * 20) - 1)
smog_filter_effectiveness = st.sidebar.selectbox("Smog Filter Effectiveness (%)", 
                                                 [i / 100.0 for i in range(10, 101, 5)], 
                                                 index=3)

# Button to visualize the adjusted AQI after changes
if st.sidebar.button("Visualize Adjusted AQI"):
    # Simulate the adjusted AQI values
    adjusted_df = simulate_aqi(df, vegetation_ratio, ev_adoption_ratio, smog_filter_effectiveness)
    
    # Plotting AQI
    st.subheader("AQI and Adjusted AQI over Time")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(adjusted_df['timestamp'], adjusted_df['AQIH'], label='Original AQI', color='blue')
    ax1.plot(adjusted_df['timestamp'], adjusted_df['AQI_Adjusted'], label='Adjusted AQI', color='cyan', linestyle='--')
    ax1.set_title('AQI and Adjusted AQI over Time')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('AQI')
    ax1.grid()
    ax1.legend()
    st.pyplot(fig1)

    # Plotting PM2.5
    st.subheader("PM2.5 and Adjusted PM2.5 over Time")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(adjusted_df['timestamp'], adjusted_df['PM2.5'], label='Original PM2.5', color='green')
    ax2.plot(adjusted_df['timestamp'], adjusted_df['PM2.5_Adjusted'], label='Adjusted PM2.5', color='lime', linestyle='--')
    ax2.set_title('PM2.5 and Adjusted PM2.5 over Time')
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('PM2.5')
    ax2.grid()
    ax2.legend()
    st.pyplot(fig2)

    # Plotting PM10
    st.subheader("PM10 and Adjusted PM10 over Time")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(adjusted_df['timestamp'], adjusted_df['PM10'], label='Original PM10', color='orange')
    ax3.plot(adjusted_df['timestamp'], adjusted_df['PM10_Adjusted'], label='Adjusted PM10', color='yellow', linestyle='--')
    ax3.set_title('PM10 and Adjusted PM10 over Time')
    ax3.set_xlabel('Timestamp')
    ax3.set_ylabel('PM10')
    ax3.grid()
    ax3.legend()
    st.pyplot(fig3)

# Option to download the adjusted DataFrame
if st.button("Download Adjusted Data as CSV"):
    adjusted_df.to_csv('Adjusted_AQI_Data.csv', index=False)
    st.success("Download ready!")

