# economic_stability.py

import streamlit as st
import pandas as pd
import json
from utils import (
    get_median_household_income,
    fetch_unemployment_data,
    get_school_rating,
    get_first_sb_geo_code,
    school_grade
)

def run():
    st.markdown("<h1 style='text-align: center;'>Economic Stability Overview</h1>", unsafe_allow_html=True)

    # Load and parse data from JSON
    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
        data = json.load(file)

    # Set up side-by-side display for Median Income and School Rating
    col1, col2 = st.columns(2)

    # Display Median Household Income
    with col1:
        st.markdown("<h2 style='text-align: center;'>Median Household Income</h2>", unsafe_allow_html=True)
        median_income = get_median_household_income("48", "113")
        st.markdown(f"<h3 style='text-align: center;'>${median_income}</h3>", unsafe_allow_html=True)

    # Display School Rating
    with col2:
        st.markdown("<h2 style='text-align: center;'>School Rating</h2>", unsafe_allow_html=True)
        postal_code = data['parcels'][0]['location']['postalCode']
        # school_rating = get_school_rating(get_first_sb_geo_code(postal_code))
        school_rating = school_grade()
        st.markdown(f"<h3 style='text-align: center;'>Rating: {school_rating}</h3>", unsafe_allow_html=True)

    # Display Unemployment Rate Over Time
    st.markdown("<h2 style='text-align: center;'>Unemployment Rate Over Time</h2>", unsafe_allow_html=True)
    city = data['parcels'][0]["location"]["locality"].capitalize()
    unemployment_data = fetch_unemployment_data(city=city)
    unemployment_df = pd.DataFrame(unemployment_data, columns=["Date", "Unemployment Rate"])
    unemployment_df["Date"] = pd.to_datetime(unemployment_df["Date"])
    unemployment_df.set_index("Date", inplace=True)
    st.line_chart(unemployment_df["Unemployment Rate"])

