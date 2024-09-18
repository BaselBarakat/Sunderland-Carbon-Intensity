import streamlit as st
import pandas as pd
from pathlib import Path
import requests
from datetime import datetime, timedelta

import pytz


# Set the title and favicon for the browser tab
st.set_page_config(page_title='Sunderland Carbon Intensity', page_icon=':earth_americas:')

# Function to load and process Carbon Intensity data
@st.cache_data
def get_carbon_data():
    """Load Carbon Intensity data from a CSV file with caching."""
    DATA_FILENAME = Path(__file__).parent / 'data/carbon.csv'
    raw_carbon_df = pd.read_csv(DATA_FILENAME, parse_dates=['from','to'], infer_datetime_format=True)

    # Convert 'from' and 'to' columns to datetime format
    raw_carbon_df['from'] = pd.to_datetime(raw_carbon_df['from'])
    raw_carbon_df['to'] = pd.to_datetime(raw_carbon_df['to'])
    #raw_carbon_df = raw_carbon_df.drop('Unnammed: 0', axis=1)
    return raw_carbon_df

# Function to get the last available timestamp from the DataFrame
def get_first_timestamp_from_df(df, timestamp_column):
    # Ensure the timestamp column is in datetime format
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    # Get the first timestamp
    first_timestamp = df[timestamp_column].min()
    return first_timestamp

# Get current UK time rounded to the nearest half hour
def get_current_uk_time_rounded():
    uk_timezone = pytz.timezone('Europe/London')
    current_time = datetime.now(uk_timezone)
    
    # Round to the nearest half-hour
    minutes = current_time.minute
    if minutes < 15:
        rounded_time = current_time.replace(minute=0, second=0, microsecond=0)
    elif 15 <= minutes < 45:
        rounded_time = current_time.replace(minute=30, second=0, microsecond=0)
    else:
        rounded_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    return rounded_time

# Main function to generate date range
def generate_date_range_from_df(df, timestamp_column):
    # Get the last timestamp from DataFrame
    start_date = get_first_timestamp_from_df(df, timestamp_column)
    
    # Get the current UK time rounded to the nearest half hour
    end_date = get_current_uk_time_rounded()
    
    # Generate date range from start_date to end_date
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    return date_range



# # Load the Carbon Intensity data
carbon_df = get_carbon_data()


timestamp_column = 'to'  # Replace with your actual timestamp column name
date_range = generate_date_range_from_df(carbon_df, timestamp_column)
# print(date_range)


# csv_file_path = 'carbon.csv'  # Replace with your CSV file path
# timestamp_column = 'to'  # Replace with your actual timestamp column name
# date_range = generate_date_range(csv_file_path, timestamp_column)
# print(date_range)


skipped = []
# Function to fetch data for a given date range
def fetch_data(start, end):
    headers = {'Accept': 'application/json'}
    url = f'https://api.carbonintensity.org.uk/regional/intensity/{start.strftime("%Y-%m-%dT%H:%MZ")}/{end.strftime("%Y-%m-%dT%H:%MZ")}/postcode/me4'
    response = requests.get(url, params={}, headers=headers)
    return response.json()

# Initialize an empty list to store records
all_records = []

# Loop through each date range and fetch data
for i in range(len(date_range) - 1):
    start = date_range[i]
    end = date_range[i + 1]
    data = fetch_data(start, end)
    
    try:
        # Extract relevant data
        entries = data['data']['data']
    except:
        # print(start)
        skipped.append(start)
        continue
    
    for entry in entries:
        record = {
            'from': entry['from'],
            'to': entry['to'],
            'forecast': entry['intensity']['forecast'],
            'index': entry['intensity']['index'],
        }
        for mix in entry['generationmix']:
            record[mix['fuel']] = mix['perc']
        all_records.append(record)

# Convert list of records to DataFrame
carbon_df = pd.DataFrame(all_records)
# -----------------------------------------------------------------------------
# Draw the page content

# Dashboard Title and Introduction
st.title(':earth_americas: Sunderland Carbon Intensity')
# st.title('Dr Basel Barakat')
st.markdown("""
### Introduction to the Sunderland Carbon Intensity Dashboard

#### Dr Basel Barakat
##### University of Sunderland
##### School of Computer Science and  Engineering
##### Faculty of Business and Technology
Welcome to the Sunderland Carbon Intensity Dashboard! This interactive platform provides a comprehensive overview of carbon emissions in Sunderland, offering real-time and historical insights into the city's carbon intensity levels.

**Carbon intensity** refers to the amount of carbon dioxide (CO₂) emissions produced per unit of energy consumed. It is a crucial metric for understanding the environmental impact of energy use and identifying opportunities for reducing greenhouse gas emissions.

**Key Features of the Dashboard:**
- **Real-Time Monitoring:** View up-to-date information on carbon intensity levels across Sunderland.
- **Historical Data Analysis:** Explore past trends in carbon intensity.
- **Interactive Visualizations:** Utilize dynamic charts, graphs, and maps to visualize data effectively.
- **Impact Assessment:** Understand how different energy sources and activities contribute to Sunderland's overall carbon footprint.

Explore the dashboard today to see how you can contribute to a sustainable future!
""")

# Add space between sections
st.write('')



# Ensure that the 'from' column is in UTC timezone
carbon_df['from'] = pd.to_datetime(carbon_df['from'], utc=True)

# carbon_df.to_csv('/data/carbon.csv')
# Get the min and max date from the DataFrame
min_date = carbon_df['from'].min()
max_date = carbon_df['from'].max()

# Streamlit slider for date range
selected_dates = st.slider('Select the date range:', 
                           min_value=min_date.to_pydatetime(), 
                           max_value=max_date.to_pydatetime(), 
                           value=(min_date.to_pydatetime(), max_date.to_pydatetime()))

# Convert the selected dates from Streamlit slider to timezone-aware datetime objects
start_date = pd.to_datetime(selected_dates[0]).tz_convert('UTC')
end_date = pd.to_datetime(selected_dates[1]).tz_convert('UTC')

# Filter the DataFrame with compatible timezone-aware datetime objects
filtered_carbon_df = carbon_df[(carbon_df['from'] >= start_date) & (carbon_df['from'] <= end_date)]

# Display filtered DataFrame
st.write(filtered_carbon_df)



# Carbon Intensity Line Chart
st.header('Carbon Intensity Over Time')
st.line_chart(filtered_carbon_df, x='from', y='forecast')

# Display summary statistics
st.header('Carbon Intensity Statistics')
st.write(filtered_carbon_df.describe())

# Display selected date range data
st.write(f"Data from {selected_dates[0].strftime('%Y-%m-%d %H:%M')} to {selected_dates[1].strftime('%Y-%m-%d %H:%M')}")
st.dataframe(filtered_carbon_df)