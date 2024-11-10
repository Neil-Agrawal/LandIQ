# zone.py
import streamlit as st
import requests
import json

def get_zoning_data_by_address(address):
    url = "https://api.lightboxre.com/v1/zoning/address"
    
    # Define the headers and parameters
    headers = {
        "accept": "application/json",
        "x-api-key": "veGcgaV8dFLPASNhazbVqMT5mL8YrXVw"
    }
    params = {
        "text": address
    }
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        st.write("Error details:", response.text)
        return None

# Streamlit App
def run():
    st.title("Zoning Data by Address")
    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
        data = json.load(file)

    # Address input field
    address = f"{data['parcels'][0]['location']['streetAddress'].capitalize()}, {data['parcels'][0]['location']['locality'].capitalize()} {data['parcels'][0]['location']['regionCode']}"

    # Fetch and display data when the button is clicked
    
    data = get_zoning_data_by_address(address)
    
    if data:
        # Display zoning data in a well-structured and readable format
        st.write("### Zoning Information:")
        
        try:
            zone_info = data['zonings'][0]
            st.write("#### Subcategory:")
            st.write(zone_info['subcategory'])
            
            # st.write("#### Permitted Use:")
            # st.write(zone_info['permittedUse'])
            
            # st.write("#### Maximum Building Height:")
            # st.write(zone_info['maximumBuildingHeight']['label'])
            # st.write(zone_info['maximumBuildingHeight']['description'])
        
        except KeyError:
            st.error("The zoning information could not be displayed properly.")
