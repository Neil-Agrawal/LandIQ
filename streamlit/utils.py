import requests
import re
import pandas as pd
from geopy.distance import geodesic
import streamlit as st

def get_parcel_data(fip, apn, api_key='MLv7H25xLA5SFudWZoCGxLXQv4WRZyY7'):
    url = f"https://api.lightboxre.com/v1/parcels/us/fips/{fip}/apn/{apn}"
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_crime_rating(city):
    df = pd.read_csv('/Users/neilagrawal/HackFinFall2024/static_data/ratings.csv')
    row =  df.loc[df['City'] == city.capitalize()]
    return row['Rating']

def rate_income(income):
    """
    Rates income on a scale from 0 to 5 based on predefined income ranges.
    Adjust these ranges as needed to reflect the distribution of income in the area.
    """
    income = int(income)
    if income < 25000:
        return 0
    elif 25000 <= income < 40000:
        return 1
    elif 40000 <= income < 55000:
        return 2
    elif 55000 <= income < 70000:
        return 3
    elif 70000 <= income < 85000:
        return 4
    else:
        return 5




def get_median_household_income(state, county, api_key="c8445bf4c6305fdccdee9a1137662c7a35fa5941"):
    # Base URL for the American Community Survey (ACS) 5-year data
    base_url = "https://api.census.gov/data/2021/acs/acs5"
    
    # Specify the variable for median household income
    variables = "B19013_001E"  # Median Household Income
    
    # Construct the API request URL
    url = f"{base_url}?get={variables}&for=county:{county}&in=state:{state}&key={api_key}"
    
    # Make the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        
        # Return the median household income from the second row and first column
        if len(data) > 1:
            return data[1][0]
        else:
            print("Data not found.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def get_first_sb_geo_code(postal_code, page=1, page_size=100, api_key = "2b1e86b638620bf2404521e6e9e1b19e"):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/address"
    
    # Define the headers and parameters
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    
    params = {
        "postalcode": postal_code,
        "page": page,
        "pagesize": page_size
    }
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Attempt to retrieve the first "SB" geo code
        try:
            sb_geo_codes = data['property'][0]['location']['geoIdV4']['SB']
            # If there are multiple SB values, return only the first one
            first_sb_geo_code = sb_geo_codes.split(",")[0].strip()
            return first_sb_geo_code
        except (KeyError, IndexError):
            print("SB geo code not found in response.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
import random
def school_grade():
    return random.choice(['A', 'B', 'C', 'D', 'F'])




def get_school_rating(geo_id, api_key = "2b1e86b638620bf2404521e6e9e1b19e"):
    url = "https://api.gateway.attomdata.com/v4/school/profile"
    
    # Define the headers and parameters
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    
    params = {
        "geoIdV4": geo_id
    }
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Attempt to retrieve the school rating
        try:
            school_rating = data['school']['detail']['schoolRating']
            return school_rating
        except (KeyError, IndexError):
            print("School rating not found in response.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


def grade_to_scale(grade):
    """
    Converts a letter grade (F to A+) with pluses and minuses to a scale from 0 to 5.
    """
    grade_scale = {
        "A+": 5,
        "A": 4.7,
        "A-": 4.3,
        "B+": 4,
        "B": 3.7,
        "B-": 3.3,
        "C+": 3,
        "C": 2.7,
        "C-": 2.3,
        "D+": 2,
        "D": 1.7,
        "D-": 1.3,
        "F": 0
    }
    
    # Convert the grade to uppercase to handle case insensitivity
    grade = grade.upper()
    
    # Return the corresponding scale value, defaulting to None if the grade is invalid
    return grade_scale.get(grade, None)


def fetch_unemployment_data(city, start_date= "2020-01-01", end_date = "2024-01-01", api_key="418c72a9e56bd5b58325065d53304c74"):
    """
    Fetches economic data from the FRED API based on the provided series ID and date range.
    
    Parameters:
        api_key (str): Your FRED API key.
        series_id (str): The series ID for the economic data you want to retrieve.
        start_date (str): The start date for the data in the format YYYY-MM-DD.
        end_date (str): The end date for the data in the format YYYY-MM-DD.
    
    Returns:
        list: A list of tuples, where each tuple contains (date, value).
    """
    if city == "Dallas" or city == "Rowlett" or city == "Richardson":
        series_id = "DALL148UR"
    elif city == "Houston" or city == "Garland":
        series_id = "HOUT148UR"
    
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    url = f"{base_url}?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        result = [(obs["date"], float(obs["value"])) for obs in observations if obs["value"] != "."]
        return result
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Error details:", response.text)
        return []

def convert_string_to_cords(polygon_str):
    coordinates = re.findall(r"[-+]?\d*\.\d+|\d+", polygon_str)
    coordinates = list(map(float, coordinates))

    # Group into tuples and swap lat-lon order
    formatted_coordinates = [
        (coordinates[i + 1], coordinates[i]) for i in range(0, len(coordinates), 2)
    ]
    return formatted_coordinates

def unemployment_rating(data):
    # Extract the unemployment rate
    date, rate = data[0]  # Assuming a single tuple in the format (date, rate)

    # Define rating based on the rate
    if rate <= 2.0:
        return 5  # Excellent
    elif rate <= 3.5:
        return 4  # Good
    elif rate <= 4.5:
        return 3  # Moderate
    elif rate <= 6.0:
        return 2  # Fair
    else:
        return 1  # Poor


def get_transportation_data(latitude, longitude, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass API query
    query = f"""
    [out:json];
    (
      node["highway"~"bus_stop|bus_station"](around:{radius},{latitude},{longitude});
      way["highway"~"bus_stop|bus_station"](around:{radius},{latitude},{longitude});
      node["public_transport"~"stop_position|station"](around:{radius},{latitude},{longitude});
      way["public_transport"~"stop_position|station"](around:{radius},{latitude},{longitude});
      node["railway"~"station|subway_entrance"](around:{radius},{latitude},{longitude});
      way["railway"~"station|subway"](around:{radius},{latitude},{longitude});
      node["amenity"="bicycle_rental"](around:{radius},{latitude},{longitude});
      way["amenity"="bicycle_rental"](around:{radius},{latitude},{longitude});
    );
    out body;
    >;
    out skel qt;
    """
    
    response = requests.get(overpass_url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        elements = data.get("elements", [])
        
        if not elements:
            return None
        
        for element in elements:
            lat = element.get("lat")
            lon = element.get("lon")
            if lat is not None and lon is not None:
                element["distance"] = geodesic((latitude, longitude), (lat, lon)).meters
            else:
                element["distance"] = float('inf')
        
        closest_elements = sorted(elements, key=lambda x: x["distance"])[:3]
        
        return closest_elements
    else:
        
        return None

        
def get_average_economic_stability(income, unemployment, school):
    return (income + unemployment + school)/3


def fetch_mortgage_rate_data(start_date="2020-01-01", end_date="2023-12-28", series_id="MORTGAGE30US",api_key = '418c72a9e56bd5b58325065d53304c74'):
    """
    Fetches mortgage rate data from the FRED API and returns it as a Pandas DataFrame.

    Parameters:
        api_key (str): Your FRED API key.
        start_date (str): Start date for the data in the format "YYYY-MM-DD".
        end_date (str): End date for the data in the format "YYYY-MM-DD".
        series_id (str): FRED series ID for the mortgage rate data. Default is "MORTGAGE30US".

    Returns:
        pd.DataFrame: DataFrame containing the date and value of mortgage rates.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    url = f"{base_url}?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        
        # Convert observations to a DataFrame
        df = pd.DataFrame(observations)
        df = df[['date', 'value']]
        df.columns = ['Date', 'Interest Rate (30-Year Fixed Mortgage)']
        
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

def rate_last_mortgage_value(df):
    """
    Rates the last mortgage rate in a DataFrame on a scale from 0 to 5.

    Parameters:
        df (pd.DataFrame): DataFrame containing the mortgage rate data with a column 
                           named 'Interest Rate (30-Year Fixed Mortgage)'.

    Returns:
        int: Rating on a scale from 0 to 5 for the last mortgage rate.
    """
    # Ensure the 'Interest Rate (30-Year Fixed Mortgage)' column exists
    if 'Interest Rate (30-Year Fixed Mortgage)' not in df.columns:
        print("DataFrame must contain 'Interest Rate (30-Year Fixed Mortgage)' column.")
        return None

    # Get the last mortgage rate value
    last_mortgage_rate = float(df['Interest Rate (30-Year Fixed Mortgage)'].iloc[-1])

    # Apply the rating scale
    if last_mortgage_rate <= 3.5:
        return 5
    elif last_mortgage_rate <= 4.5:
        return 4
    elif last_mortgage_rate <= 5.5:
        return 3
    elif last_mortgage_rate <= 6.5:
        return 2
    elif last_mortgage_rate <= 7.5:
        return 1
    else:
        return 0


def get_county_data_house_price(county_name, state_abbreviation):
    data = pd.read_csv("/Users/neilagrawal/HackFinFall2024/static_data/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month (1).csv")
    # Filter the DataFrame for the specified county and state
    result = data[(data['RegionName'] == f'{county_name} County') & (data['State'] == state_abbreviation)]
    return result

def get_preforeclosure_count( apn, api_key="2b1e86b638620bf2404521e6e9e1b19e", county="dallas", state="TX"):
    url = "https://api.gateway.attomdata.com/property/v3/preforeclosuredetails"
    
    # Define the headers and parameters
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    
    params = {
        "apn": apn,
        "county": county,
        "state": state
    }
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        try:
            # Count the number of entries in "Default" and "Auction" arrays
            default_count = len(data['PreforeclosureDetails']['Default'])
            auction_count = len(data['PreforeclosureDetails']['Auction'])
            total_foreclosures = default_count + auction_count
            return total_foreclosures
        except (KeyError, TypeError):
            print("Foreclosure data not found in response.")
            return 0
    else:
        print(f"Error: {response.status_code}")
        return None

def calculate_rank_house_price(latest_price):
    data = pd.read_csv("/Users/neilagrawal/HackFinFall2024/static_data/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month (1).csv")
    # Get the latest prices for all cities
    all_latest_prices = data.iloc[:, -1]
    
    # Calculate percentiles and assign ranks based on price quintiles
    rank = pd.qcut(all_latest_prices, 5, labels=[1, 2, 3, 4, 5])
    city_rank = rank[all_latest_prices == latest_price].values[0]
    return city_rank

def get_sales_trend_2023():
    mock_data = {
        "salesTrends": [
            {
                "dateRange": {"start": "2018", "end": "2018"},
                "salesTrend": {
                    "homeSaleCount": 1200,
                    "avgSalePrice": 250000
                }
            },
            {
                "dateRange": {"start": "2019", "end": "2019"},
                "salesTrend": {
                    "homeSaleCount": 1300,
                    "avgSalePrice": 260000
                }
            },
            {
                "dateRange": {"start": "2020", "end": "2020"},
                "salesTrend": {
                    "homeSaleCount": 1100,
                    "avgSalePrice": 255000
                }
            },
            {
                "dateRange": {"start": "2021", "end": "2021"},
                "salesTrend": {
                    "homeSaleCount": 1400,
                    "avgSalePrice": 270000
                }
            },
            {
                "dateRange": {"start": "2022", "end": "2022"},
                "salesTrend": {
                    "homeSaleCount": 1500,
                    "avgSalePrice": 280000
                }
            }
        ]
    }
    
    try:
        # Find the entry for 2022
        sales_trend_2022 = next(
            entry["salesTrend"] for entry in mock_data["salesTrends"]
            if entry["dateRange"]["start"] == "2022" and entry["dateRange"]["end"] == "2022"
        )
        home_sale_count = sales_trend_2022['homeSaleCount']
        avg_sale_price = sales_trend_2022['avgSalePrice']
        
        return home_sale_count, avg_sale_price
    
    except (KeyError, StopIteration):
        print("Sales trend data for 2022 not found in response.")
        return None, None



def get_sales_trend_2022(geo_id):
    url = "https://api.gateway.attomdata.com/v4/transaction/salestrend"
    interval = "yearly"
    start_year = 2018
    end_year = 2022
    api_key = "2b1e86b638620bf2404521e6e9e1b19e"
    
    # Define the headers and parameters
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
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        try:
            # Find the entry for 2022
            sales_trend_2022 = next(
                entry["salesTrend"] for entry in data["salesTrends"]
                if entry["dateRange"]["start"] == "2022" and entry["dateRange"]["end"] == "2022"
            )
            home_sale_count = sales_trend_2022['homeSaleCount']
            avg_sale_price = sales_trend_2022['avgSalePrice']
            
            return home_sale_count, avg_sale_price
        
        except (KeyError, StopIteration):
            st.error("Sales trend data for 2022 not found in response.")
            return None, None
    else:
        st.error(f"Error: {response.status_code}")
        return None, None

def get_geoid(postal_code, page=1, page_size=100, api_key = "2b1e86b638620bf2404521e6e9e1b19e"):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/address"
    
    # Define the headers and parameters
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    
    params = {
        "postalcode": postal_code,
        "page": page,
        "pagesize": page_size
    }
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Attempt to retrieve the first "SB" geo code
        return data['property'][0]['location']['geoIdV4']['N2']
    else:
        print(f"Error: {response.status_code}")
        return None