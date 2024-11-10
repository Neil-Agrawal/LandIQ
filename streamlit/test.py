from utils import get_median_household_income, get_first_sb_geo_code, get_school_rating, fetch_unemployment_data, convert_string_to_cords, unemployment_rating, get_transportation_data
import json
import requests

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

data = get_geoid(75056)
print(data['property'][0]['location']['geoIdV4']['N2'])