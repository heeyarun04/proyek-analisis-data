import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

##########################
sns.set(style='dark')

# Page configuration
st.set_page_config(
    page_title="Air Quality in Beijing",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded")

# Title of the dashboard
st.title('Air Quality Analysis Dashboard :sparkles:')

# Load dataset
all_df = pd.read_csv('all_data.csv')

# Adding a sidebar for interactive inputs
st.sidebar.header('User Input Features')

# About me
st.markdown("""
### About Me
- **Name**: Hiyarunnisa Kahes Waypi
- **Email Address**: yarun.kawa@gmail.com
- **Dicoding ID**: [Hyarun](https://www.dicoding.com/users/heeyarun/)

### Project Overview
This dashboard presents an analysis of air quality data, particularly focusing on PM2.5 levels, from the station selected. The project aims to uncover trends and the impact of different weather conditions on air quality. Insights from this analysis can be valuable for environmental studies and public health monitoring.
""")

# Let users select a year and month to view data
selected_year = st.sidebar.selectbox('Select Year', list(all_df['year'].unique()))
selected_month = st.sidebar.selectbox('Select Month', list(all_df['month'].unique()))
selected_station = st.sidebar.selectbox('Select Station', list(all_df['station'].unique()))

# Filter data based on the selected year and month
data_filtered = all_df[(all_df['year'] == selected_year) & (all_df['month'] == selected_month) & (all_df['station'] == selected_station)].copy()

# Displaying data statistics
st.subheader('Data Overview for Selected Period')
st.write(data_filtered.describe())

# Line chart for PM2.5 levels for Selected Station per Month All Year
st.subheader('Average PM2.5 Distribution among Station per Month from 2013-2017')
filtered_data = all_df[all_df['station'] == selected_station]
if not filtered_data.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_avg_pm25 = filtered_data.groupby(['year', 'month'])['PM2.5'].mean().reset_index()
    monthly_avg_pm25['date'] = pd.to_datetime(monthly_avg_pm25[['year', 'month']].assign(day=1))
    ax.plot(monthly_avg_pm25['date'], monthly_avg_pm25['PM2.5'], marker='o')
    ax.set(xlabel='Month', ylabel='Average PM2.5',
           title=f'Average PM2.5 Distribution per Month for {selected_station} (All Years)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
else:
    st.write(f'No data available for {selected_station}. Please select another station.')


# Correlation heatmap for the selected month and station
st.subheader('Correlation Heatmap of Air Quality Indicators')
corr = data_filtered[['PM2.5', 'NO2', 'SO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
plt.title('Correlation Heatmap')
st.pyplot(fig)


# Hourly Averages Heatmap
st.subheader('Hourly Averages of PM2.5')
try:
    # Ensure correct data types and handle missing values
    all_df['hour'] = all_df['hour'].astype(int)
    all_df['PM2.5'] = pd.to_numeric(all_df['PM2.5'], errors='coerce')
    all_df['PM2.5'].ffill(inplace=True)

    # Calculate hourly averages
    hourly_avg = all_df.groupby('hour')['PM2.5'].mean()

    # Plotting
    fig, ax = plt.subplots()
    sns.heatmap([hourly_avg.values], ax=ax, cmap='coolwarm')
    plt.title('Hourly Averages of PM2.5')
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error in plotting hourly averages: {e}")

# Wind Direction Analysis
st.subheader('Wind Direction Analysis')
wind_data = data_filtered.groupby('wd')['PM2.5'].mean()
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, polar=True)
theta = np.linspace(0, 2 * np.pi, len(wind_data))
bars = ax.bar(theta, wind_data.values, align='center', alpha=0.5)
plt.title('PM2.5 Levels by Wind Direction')
st.pyplot(fig)

# Rainfall vs. Air Quality
st.subheader('Rainfall vs. PM2.5 Levels')
fig, ax = plt.subplots()
sns.scatterplot(x='RAIN', y='PM2.5', data=data_filtered, ax=ax)
plt.title('Rainfall vs. PM2.5 Levels')
st.pyplot(fig)
