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

###2. Wilayah mana yang memiliki indeks kualitas udara terbaik dan wilayah mana yang terburuk?
st.title('Nilai Polutan di Setiap Stasiun')
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=all_df.melt(id_vars='station'), x='value', y='station', hue='variable', orient='h')
plt.xlabel('Nilai Polutan')
plt.ylabel('Stasiun')
plt.legend(title='Polutan')
for p in ax.patches:
    width = p.get_width()  # Get the width of the bar
    height = p.get_height()  # Get the height of the bar
    x, y = p.get_xy()  # Get the initial x and y coordinates
    if width > 0.1:  # Add text only if the width of the bar is greater than 0.1
        plt.annotate(f'{width:.2f}',
                     (x + width, y + height),
                     xytext=(5, 6),
                     textcoords='offset points',
                     ha='left',
                     va='center',
                     fontsize=8)
st.pyplot(plt)

###Kesimpulan
kesimpulan='''
1. Dari tahun 2013 hingga 2017 awal mengalami fluktuasi naik turun. Ini bisa disebabkan oleh faktor-faktor seperti perubahan dalam aktivitas industri atau transportasi, cuaca ekstrem, atau kegagalan dalam penerapan kebijakan pengendalian emisi')
2. Wanliu mempunyai polutan yang paling tinggi dan Dingling mempunyai polutan paling rendah, meskipun nilai ozon di Wanliu paling rendah
'''
st.markdown(kesimpulan)
