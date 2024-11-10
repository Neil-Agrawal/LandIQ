import streamlit as st
import requests

# Function to fetch sales trend data
def get_sales_trend_2022(api_key, geo_id, interval="yearly", start_year=2018, end_year=2022):
    url = "https://api.gateway.attomdata.com/v4/transaction/salestrend"
    
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    
    params = {
        "geoIdV4": geo_id,
        "interval": interval,
        "startyear": start_year,
        "endyear": end_year
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        try:
            sales_trend_2022 = next(
                entry["salesTrend"] for entry in data["salesTrends"]
                if entry["dateRange"]["start"] == "2022" and entry["dateRange"]["end"] == "2022"
            )
            return sales_trend_2022
        except (KeyError, StopIteration):
            st.error("Sales trend data for 2022 not found in response.")
            return None
    else:
        st.error(f"Error: {response.status_code}")
        return None

# Streamlit page configuration
st.set_page_config(page_title="Sales Trend Analysis 2022", page_icon="📊", layout="centered")
st.title("📊 Comparative Market Analysis (CMA) for 2022")
st.write("Use this tool to analyze the sales trend data for a given location and estimate the Fair Market Value (FMV) based on the average sale price in 2022.")

# User inputs for API key, Geo ID, and other parameters
with st.sidebar:
    st.header("Input Parameters")
    api_key = st.text_input("API Key", type="password")
    geo_id = st.text_input("Geo ID")
    interval = st.selectbox("Interval", ["yearly", "monthly", "quarterly"], index=0)
    start_year = st.number_input("Start Year", value=2018, min_value=2000, max_value=2022)
    end_year = st.number_input("End Year", value=2022, min_value=2000, max_value=2022)

# Button to fetch data
if st.button("Fetch Sales Trend Data"):
    if api_key and geo_id:
        sales_trend_2022 = get_sales_trend_2022(api_key, geo_id, interval, start_year, end_year)
        
        if sales_trend_2022:
            # Display Sales Trend Data for 2022
            st.subheader("Sales Trend Data for 2022")
            home_sale_count = sales_trend_2022['homeSaleCount']
            avg_sale_price = sales_trend_2022['avgSalePrice']
            st.write("### Key Metrics")
            st.write(f"**Home Sale Count:** {home_sale_count}")
            st.write(f"**Average Sale Price:** ${avg_sale_price:,.2f}")

            # User input for number of houses to build
            st.subheader("FMV Calculation")
            num_houses_to_build = st.number_input("Number of houses you plan to build", min_value=1, value=1)
            fmv = num_houses_to_build * avg_sale_price

            # Display FMV result
            st.write("### Estimated Fair Market Value (FMV) of the Land")
            st.write(f"**Number of Houses Planned:** {num_houses_to_build}")
            st.write(f"**Total FMV:** ${fmv:,.2f}")
    else:
        st.warning("Please enter both API Key and Geo ID to fetch data.")