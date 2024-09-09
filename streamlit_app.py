
import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon for the browser tab
st.set_page_config(page_title='Sunderland Carbon Intensity', page_icon=':earth_americas:')

# Function to load and process GDP data
@st.cache_data
def get_gdp_data():
    """Load GDP data from a CSV file with caching."""
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    
    # Define year range
    MIN_YEAR, MAX_YEAR = 2018, 2024
    
    # Reshape data from wide to long format
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP'
    )
    
    # Convert 'Year' to numeric
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    
    return gdp_df

# Load the GDP data
gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the page content

# Dashboard Title and Introduction
st.title(':earth_americas: Sunderland Carbon Intensity')
st.markdown("""
### Introduction to the Sunderland Carbon Intensity Dashboard

Welcome to the Sunderland Carbon Intensity Dashboard! This interactive platform provides a comprehensive overview of carbon emissions in Sunderland, offering real-time and historical insights into the city's carbon intensity levels.

Carbon intensity refers to the amount of carbon dioxide (CO₂) emissions produced per unit of energy consumed. It is a crucial metric for understanding the environmental impact of energy use and identifying opportunities for reducing greenhouse gas emissions.

**Key Features of the Dashboard:**
- **Real-Time Monitoring:** View up-to-date information on carbon intensity levels across Sunderland.
- **Historical Data Analysis:** Explore past trends in carbon intensity.
- **Interactive Visualizations:** Utilize dynamic charts, graphs, and maps to visualize data effectively.
- **Impact Assessment:** Understand how different energy sources and activities contribute to Sunderland's overall carbon footprint.

By tracking carbon intensity, Sunderland can promote cleaner energy, enhance sustainability planning, and engage the community in reducing emissions.

Explore the dashboard today to see how you can contribute to a sustainable future!
""")

# Add space between sections
st.write('')

# Year selection slider
min_value, max_value = gdp_df['Year'].min(), gdp_df['Year'].max()
from_year, to_year = st.slider('Select the year range:', min_value=min_value, max_value=max_value, value=[min_value, max_value])

# Country selection
countries = gdp_df['Country Code'].unique()
selected_countries = st.multiselect('Select countries to view:', countries, ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# Warn if no country is selected
if not selected_countries:
    st.warning("Please select at least one country to view the data.")

# Filter the data based on user input
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries)) &
    (gdp_df['Year'] >= from_year) &
    (gdp_df['Year'] <= to_year)
]

# GDP Line Chart
st.header('GDP over time')
st.line_chart(filtered_gdp_df, x='Year', y='GDP', color='Country Code')

# Display GDP Metrics
st.header(f'GDP in {to_year}')

# Display metrics for each selected country
cols = st.columns(4)
for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]
    with col:
        first_gdp = gdp_df[(gdp_df['Country Code'] == country) & (gdp_df['Year'] == from_year)]['GDP'].iat[0] / 1e9
        last_gdp = gdp_df[(gdp_df['Country Code'] == country) & (gdp_df['Year'] == to_year)]['GDP'].iat[0] / 1e9

        if math.isnan(first_gdp):
            growth, delta_color = 'n/a', 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(label=f'{country} GDP', value=f'{last_gdp:,.0f}B', delta=growth, delta_color=delta_color)




# import streamlit as st
# import pandas as pd
# import math
# from pathlib import Path

# # Set the title and favicon that appear in the Browser's tab bar.
# st.set_page_config(
#     page_title='Sunderland Carbon Intensity',
#     page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
# )

# # -----------------------------------------------------------------------------
# # Declare some useful functions.

# @st.cache_data
# def get_gdp_data():
#     """Grab GDP data from a CSV file.

#     This uses caching to avoid having to read the file every time. If we were
#     reading from an HTTP endpoint instead of a file, it's a good idea to set
#     a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
#     """

#     # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
#     DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
#     raw_gdp_df = pd.read_csv(DATA_FILENAME)

#     MIN_YEAR = 1960
#     MAX_YEAR = 2022

#     # The data above has columns like:
#     # - Country Name
#     # - Country Code
#     # - [Stuff I don't care about]
#     # - GDP for 1960
#     # - GDP for 1961
#     # - GDP for 1962
#     # - ...
#     # - GDP for 2022
#     #
#     # ...but I want this instead:
#     # - Country Name
#     # - Country Code
#     # - Year
#     # - GDP
#     #
#     # So let's pivot all those year-columns into two: Year and GDP
#     gdp_df = raw_gdp_df.melt(
#         ['Country Code'],
#         [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
#         'Year',
#         'GDP',
#     )

#     # Convert years from string to integers
#     gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

#     return gdp_df

# gdp_df = get_gdp_data()

# # -----------------------------------------------------------------------------
# # Draw the actual page

# # Set the title that appears at the top of the page.
# '''
# # :earth_americas: Sunderland Carbon Intensity

# Introduction to the Sunderland Carbon Intensity Dashboard

# Welcome to the Sunderland Carbon Intensity Dashboard! This interactive platform is designed to provide a comprehensive overview of carbon emissions in Sunderland, offering real-time and historical insights into the city's carbon intensity levels.

# Carbon intensity refers to the amount of carbon dioxide (CO₂) emissions produced per unit of energy consumed. It is a crucial metric for understanding the environmental impact of energy use and helps identify opportunities for reducing greenhouse gas emissions. The Sunderland Carbon Intensity Dashboard brings together data from various sources to monitor the city’s carbon footprint, track changes over time, and support decision-making for a more sustainable future.
# Key Features of the Dashboard

# Real-Time Monitoring: View up-to-date information on carbon intensity levels across Sunderland, helping residents, businesses, and policymakers understand current emissions and take timely action.

# Historical Data Analysis: Explore past trends in carbon intensity, analyze patterns over different time frames, and identify key periods of high or low emissions.

# Interactive Visualizations: Utilize a range of dynamic charts, graphs, and maps to visualize data effectively, making complex information easy to understand and actionable.

# Impact Assessment: Understand how different energy sources and activities contribute to Sunderland's overall carbon footprint, aiding in the development of targeted strategies for emissions reduction.

# Why Monitor Carbon Intensity?

# Tracking carbon intensity is essential for achieving local and national climate goals. By monitoring this metric, Sunderland can:

# Promote Cleaner Energy: Encourage the use of renewable energy sources and reduce reliance on fossil fuels.

# Enhance Sustainability Planning: Support the city’s efforts to become more sustainable by providing data-driven insights for urban planning, transport, and energy policies.

# Engage the Community: Raise awareness among residents and businesses about their carbon footprint and inspire collective action towards reducing emissions.

# Conclusion

# The Sunderland Carbon Intensity Dashboard is a valuable tool for anyone interested in understanding and reducing the city’s carbon footprint. Whether you are a resident, business owner, or policymaker, this dashboard provides the data and insights needed to make informed decisions for a greener Sunderland. Explore the dashboard today to see how you can contribute to a sustainable future!
# '''

# # Add some spacing
# ''
# ''

# min_value = gdp_df['Year'].min()
# max_value = gdp_df['Year'].max()

# from_year, to_year = st.slider(
#     'Which years are you interested in?',
#     min_value=min_value,
#     max_value=max_value,
#     value=[min_value, max_value])

# countries = gdp_df['Country Code'].unique()

# if not len(countries):
#     st.warning("Select at least one country")

# selected_countries = st.multiselect(
#     'Which countries would you like to view?',
#     countries,
#     ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# ''
# ''
# ''

# # Filter the data
# filtered_gdp_df = gdp_df[
#     (gdp_df['Country Code'].isin(selected_countries))
#     & (gdp_df['Year'] <= to_year)
#     & (from_year <= gdp_df['Year'])
# ]

# st.header('GDP over time', divider='gray')

# ''

# st.line_chart(
#     filtered_gdp_df,
#     x='Year',
#     y='GDP',
#     color='Country Code',
# )

# ''
# ''


# first_year = gdp_df[gdp_df['Year'] == from_year]
# last_year = gdp_df[gdp_df['Year'] == to_year]

# st.header(f'GDP in {to_year}', divider='gray')

# ''

# cols = st.columns(4)

# for i, country in enumerate(selected_countries):
#     col = cols[i % len(cols)]

#     with col:
#         first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
#         last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
#         )
