# transpaccess.py
import streamlit as st
import json
from utils import get_transportation_data

def run():
    # Function to get transportation data
    # Load data from JSON file
    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
        data = json.load(file)
    latitude = data['parcels'][0]['location']['representativePoint']['latitude']
    longitude = data['parcels'][0]['location']['representativePoint']['longitude']
    city = data['parcels'][0]["location"]["locality"].capitalize()
    # Streamlit page configuration
    st.title("🚍 Transportation Infrastructure Overview")
    st.write("Get insights into nearby public transportation infrastructure within a specified radius.")

    # Sidebar
    with st.sidebar:
        st.header("Search Parameters")
        st.write(f"**Location:** {city}, TX")
        st.write(f"**Coordinates:** ({latitude}, {longitude})")
        
        # Radius slider
        radius = st.slider("Select Radius (in meters)", min_value=500, max_value=5000, value=2000, step=500)
        st.write(f"**Radius:** {radius} meters")

    # Display Header
    st.markdown("---")
    st.header("Nearby Transportation Facilities")
    st.write("### 3 Closest Transportation Infrastructure Elements:")

    # Fetch and display data
    transportation_data = get_transportation_data(latitude, longitude, radius)

    if transportation_data:
        for i, element in enumerate(transportation_data, start=1):
            # Identify transportation type
            tags = element.get("tags", {})
            if "bus_stop" in tags.get("highway", ""):
                transportation_type = "🚏 Bus Stop"
            elif "station" in tags.get("railway", ""):
                transportation_type = "🚉 Train Station"
            elif "subway_entrance" in tags.get("railway", ""):
                transportation_type = "🚇 Subway Entrance"
            elif "bicycle_rental" in tags.get("amenity", ""):
                transportation_type = "🚲 Bicycle Rental"
            else:
                transportation_type = "🚏 Bus Stop"
            
            distance = element.get("distance", "N/A")
            
            # Display element information in a styled format
            st.markdown(f"#### {i}. {transportation_type}")
            st.write(f"**Distance**: {distance:.2f} meters")
            st.markdown("---")  # Divider for each element
    else:
        st.warning("No transportation data found in the specified area.")

    # Footer section
    st.markdown(" ")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center>Powered by Streamlit | Data provided by OpenStreetMap & Overpass API</center>", unsafe_allow_html=True)
