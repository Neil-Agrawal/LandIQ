# crime.py
import json
import streamlit as st
import pandas as pd

def run():

    # Specify the path to your JSON file
    file_path = '/Users/neilagrawal/HackFinFall2024/static_data/output.json'

    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    city = data['parcels'][0]["location"]["locality"].capitalize()
    st.markdown(f"<h2 style='text-align: center;'>Detailed Crime Statistics for {city}</h2>", unsafe_allow_html=True)

    

    # Load the CSV file
    df = pd.read_csv('/Users/neilagrawal/HackFinFall2024/static_data/modified_crime.csv')

    # Check if a city name has been entered
    if city:
        # Filter the DataFrame for the specified city
        city_data = df[df['City'] == city]

        if not city_data.empty:
            # Drop the "City" column to plot only numerical data
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            city_data = city_data.drop(columns=['City','Population','Total Offenses']).squeeze()
            city_data_df = pd.DataFrame({
            "Columns": city_data.index,
            "Values": city_data.values
            })
            city_data_df.set_index("Columns", inplace=True)
            # Display the data as a bar chart using Streamlit's bar_chart
            st.bar_chart(city_data)
        else:
            st.warning(f"No data found for city: {city}")
