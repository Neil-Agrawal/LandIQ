# financial.py
import streamlit as st
import pandas as pd
import json
from utils import fetch_mortgage_rate_data, get_county_data_house_price, get_preforeclosure_count

def run():
    st.title("Financial Overview")
    with open("/Users/neilagrawal/HackFinFall2024/static_data/output.txt", "r") as file:
        content = file.read()
    # st.write(int(content))
    st.header(f"Preforeclosure Count for this property")
    # st.header(get_preforeclosure_count(content))
    st.header(0)
    df = fetch_mortgage_rate_data()
    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
        data = json.load(file)

    df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is in datetime format
    df.set_index('Date', inplace=True)  # Set Date as the index for better plotting
    city = data['parcels'][0]["location"]["locality"].capitalize()
    st.header(f"Mortgage Rate Over Time")
    # Display the line chart
    st.line_chart(df['Interest Rate (30-Year Fixed Mortgage)'], height = 300)

    st.header(f"House Prices Over Time for Dallas County")

    # Inputs for county and state
    county_name = "Dallas"
    state_abbreviation = "TX"

    # Retrieve and plot data
    county_data = get_county_data_house_price(county_name, state_abbreviation)

    if not county_data.empty:
        # Extract date columns (assuming they start after the initial columns)
        date_columns = county_data.columns[9:]  # Adjust if necessary
        time_series_data = county_data[date_columns].T  # Transpose for plotting
        time_series_data.columns = ['House Price Index']  # Rename for clarity
        time_series_data.index = pd.to_datetime(time_series_data.index)  # Convert to datetime index

        # Plot on Streamlit
        st.line_chart(time_series_data)
    else:
        st.write("No data found for the specified county and state.")

    