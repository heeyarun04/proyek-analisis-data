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

###1. Bagaimana tren tingkat polutan dari tahun ke tahun?

st.subheader('Average PM2.5 Distribution per Month (2013-2017)')
fig, ax = plt.subplots(figsize=(12, 6))
for station, station_data in all_df.groupby('station'):
    filtered_data = station_data[(station_data['year'] >= 2013) & (station_data['year'] <= 2017)]
    monthly_avg_pm25 = filtered_data.groupby(['year', 'month'])['PM2.5'].mean().reset_index()
    monthly_avg_pm25['date'] = pd.to_datetime(monthly_avg_pm25[['year', 'month']].assign(day=1))
    ax.plot(monthly_avg_pm25['date'], monthly_avg_pm25['PM2.5'], marker='o', label=station)
ax.set_xlabel('Month')
ax.set_ylabel('Average PM2.5')
ax.set_title('Average PM2.5 Distribution per Month (2013-2017)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.legend()
ax.grid(True)
st.pyplot(fig)
