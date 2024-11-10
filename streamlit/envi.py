# envi.py
import streamlit as st
import requests
import json

def run():
    # Set up the page configuration

    # Title and description
    st.title("🌱 Environmental Dashboard")
    st.markdown("This dashboard provides information on soil conditions, risk indices, and air quality based on your input.")

    # --- Soil Conditions Section ---
    st.header("🌡️ Soil Conditions")
    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
            data = json.load(file)
    # Input for coordinates
    latitude_soil = data['parcels'][0]['location']['representativePoint']['latitude']
    longitude_soil = data['parcels'][0]['location']['representativePoint']['longitude'] 

    # Function to get soil conditions from the AgroMonitoring API
    def get_soil_conditions(api_key, latitude, longitude):
        base_url = "http://api.agromonitoring.com/agro/1.0/soil"
        params = {"lat": latitude, "lon": longitude, "appid": api_key}
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            # Convert temperature from Kelvin to Celsius
            soil_temperature_kelvin = data.get("t0")
            soil_temperature_celsius = soil_temperature_kelvin - 273.15 if soil_temperature_kelvin is not None else None
            soil_conditions = {
                "Latitude": data.get("lat"),
                "Longitude": data.get("lon"),
                "Soil Temperature (°C)": round(soil_temperature_celsius, 2) if soil_temperature_celsius is not None else None,
                "Soil Moisture (%)": data.get("moisture")
            }
            return soil_conditions
        else:
            return {"Status Code": response.status_code, "Error": response.text}

    # Button to fetch soil conditions
    api_key = "8e616fc17b0fd551dffd01410cde668d"  # Your API key
    soil_data = get_soil_conditions(api_key, latitude_soil, longitude_soil)
    if "Error" in soil_data:
        st.error(f"Error: {soil_data['Error']}")
        st.write(f"Status Code: {soil_data['Status Code']}")
    else:
        st.write(f"**Soil Temperature (°C)**: {soil_data['Soil Temperature (°C)']} °C")
        st.write(f"**Soil Moisture (%)**: {soil_data['Soil Moisture (%)']} %")

    # --- Risk Index Section ---
    st.header("🌐 Risk Index Dashboard")

    with open('/Users/neilagrawal/HackFinFall2024/static_data/output.json', 'r') as file:
        data = json.load(file)

    # Address input field
    address = f"{data['parcels'][0]['location']['streetAddress'].capitalize()}, {data['parcels'][0]['location']['locality'].capitalize()} {data['parcels'][0]['location']['regionCode']}"


    # Function to get risk index data from the API
    base_url = "https://api.lightboxre.com/v1/riskindexes/address/search"
    url = f"{base_url}?text={address.replace(' ', '%20')}"
    headers = {"accept": "application/json", "x-api-key": "veGcgaV8dFLPASNhazbVqMT5mL8YrXVw"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Extract hazard data
        hazards = {
            "Coastal Flooding": data["nris"][0]['coastalFlooding'],
            "Cold Wave": data["nris"][0]['coldWave'],
            "Drought": data["nris"][0]['drought'],
            "Earthquake": data["nris"][0]['earthquake'],
            "Hail": data["nris"][0]['hail'],
            "Heat Wave": data["nris"][0]['heatWave'],
            "Hurricane": data["nris"][0]['hurricane'],
            "Ice Storm": data["nris"][0]['iceStorm'],
            "Landslide": data["nris"][0]['landslide'],
            "Tornado": data["nris"][0]['tornado'],
            "Tsunami": data["nris"][0]['tsunami'],
            "Volcanic Activity": data["nris"][0]['volcanicActivity'],
            "Wildfire": data["nris"][0]['wildfire'],
        }

        # Function to safely convert values to floats
        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        # Sort hazards by risk index score
        sorted_hazards = sorted(
            hazards.items(),
            key=lambda x: safe_float(x[1]['hazardTypeRiskIndex']['score']),
            reverse=True
        )

        # Function to display hazard information
        def display_hazard(column, hazard_name, details):
            score = safe_float(details['hazardTypeRiskIndex']['score'])
            if score >= 7:
                color = "red"
            elif 4 <= score < 7:
                color = "orange"
            else:
                color = "green"

            with column:
                st.markdown(
                    f"<div style='text-align: center; font-size: 28px; font-weight: bold; color: {color};'>{hazard_name}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='text-align: center; font-size: 18px; font-weight: normal; color: {color};'>{score:.2f}</div>",
                    unsafe_allow_html=True
                )

        # Display sorted hazards in a 3-column grid
        st.divider()
        for i in range(0, len(sorted_hazards), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(sorted_hazards):
                    hazard_name, details = sorted_hazards[i + j]
                    display_hazard(cols[j], hazard_name, details)
    else:
        st.error(f"Request failed with status code: {response.status_code}")
        st.write(response.text)

    # --- Air Quality Section ---
    st.header("💨 Air Quality")

    # Input fields for latitude and longitude
    latitude_air = latitude_soil
    longitude_air = longitude_soil


    # Function to get air quality information
    def get_simple_air_quality_info(lat, lon, api_key="adec45fb-b3c2-46f4-9512-bb7535c8e90b"):
        url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json().get("data", {})
            if not data:
                st.error("No data available.")
                return

            # Extracting important information
            location_info = {
                "City": data.get("city"),
                "State": data.get("state"),
                "Country": data.get("country")
            }

            current_weather = data.get("current", {}).get("weather", {})
            weather_info = {
                "Temperature (°C)": current_weather.get("tp"),
                "Pressure (hPa)": current_weather.get("pr"),
                "Humidity (%)": current_weather.get("hu"),
                "Wind Speed (m/s)": current_weather.get("ws"),
                "Wind Direction (°)": current_weather.get("wd"),
            }

            current_pollution = data.get("current", {}).get("pollution", {})
            pollution_info = {
                "AQI (US)": current_pollution.get("aqius"),
                "Main Pollutant (US)": current_pollution.get("mainus"),
                "AQI (China)": current_pollution.get("aqicn"),
                "Main Pollutant (China)": current_pollution.get("maincn")
            }

            st.subheader("Current Pollution Levels")
            for key, value in pollution_info.items():
                st.write(f"**{key}**: {value}")

        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.write(response.text)

    # Button to fetch air quality information
    get_simple_air_quality_info(latitude_air, longitude_air)
