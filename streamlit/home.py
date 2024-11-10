# Import necessary libraries
import streamlit as st
import json
from streamlit_folium import st_folium
import folium
from utils import get_parcel_data, get_crime_rating, get_median_household_income, convert_string_to_cords, get_average_economic_stability, get_school_rating, get_first_sb_geo_code, grade_to_scale, unemployment_rating, fetch_unemployment_data, rate_income,fetch_mortgage_rate_data,rate_last_mortgage_value
from utils import calculate_rank_house_price, get_county_data_house_price, get_sales_trend_2022, get_geoid, school_grade, get_sales_trend_2023

def run():
    # Set the title of the app
    st.title("Title")

    # Add an input field for user text
    apn = st.text_input("Enter the APN:")
    fip = st.text_input("Enter the FIP:")
    # Check if there’s input, then process it
    if apn and fip:
        col1, col2= st.columns(2)

        
        data = get_parcel_data(fip, apn)
        filename = "/Users/neilagrawal/HackFinFall2024/static_data/output.json"
        postal = data['parcels'][0]['location']['postalCode']
        with open("/Users/neilagrawal/HackFinFall2024/static_data/output.txt", "w") as file:
            file.write(apn)
        # Write data to JSON file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        city = data['parcels'][0]["location"]["locality"].capitalize()
        print(city)
        with col1:
            st.header("Crime Rating")
            st.header(f'{get_crime_rating(city).iloc[0]}/5')

        income_rating = rate_income(get_median_household_income(fip[0:2],fip[2:]))
        # school_rating = grade_to_scale(get_school_rating(get_first_sb_geo_code(postal)))
        school_rating = grade_to_scale(school_grade())
        unemployment_rate = unemployment_rating(fetch_unemployment_data(city,'2024-09-01','2024-09-01'))
        with col2:
            st.header("Economic Stability")
            st.header(f'{round(get_average_economic_stability(income_rating, school_rating, unemployment_rate),2)}/5')

        
        mortgage_rating = rate_last_mortgage_value(fetch_mortgage_rate_data())
        price_rating = calculate_rank_house_price(get_county_data_house_price("Dallas","TX").iloc[:, -1].values[0])
        with col1:
            st.header("Financial Stability")
            st.header(f'{(mortgage_rating+price_rating)/2}/5')
        # Define your coordinates for the polygon (in (latitude, longitude) format)
        coordinates = convert_string_to_cords(data['parcels'][0]['location']['geometry']['wkt'])

        with col2:
            st.header("Environmental Impact")
            st.header(f'3.2/5')

        # geo_id = get_geoid(postal)
        # if geo_id:
            # Get sales trend data for 2022
            # home_sale_count, avg_sale_price = get_sales_trend_2022(geo_id)
        home_sale_count, avg_sale_price = get_sales_trend_2023()
        if home_sale_count is not None and avg_sale_price is not None:
            st.title("Comparative Market Analysis (CMA)")
            st.write("=========================================")
            st.write(f"Home Sale Count: {home_sale_count}")
            st.write(f"Average Sale Price: ${avg_sale_price:,.2f}")
            
            # User input for number of houses they plan to build
            num_houses_to_build = st.number_input("Enter the number of houses you plan to build:", min_value=1, step=1)
            
            # Calculate FMV and display
            if num_houses_to_build:
                fmv = num_houses_to_build * avg_sale_price
                st.subheader("Estimated Fair Market Value (FMV) of the Land")
                st.write("=========================================")
                st.write(f"Number of Houses Planned: {num_houses_to_build}")
                st.write(f"Total FMV: ${fmv:,.2f}")

        # Initialize the Streamlit app
        st.title("Map of Plot of Land")

        # Create a map object with an arbitrary starting point
        m = folium.Map(location=coordinates[0], zoom_start=15)

        # Create the polygon
        polygon = folium.Polygon(
            locations=coordinates,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.4
        ).add_to(m)

        # Use fit_bounds to auto-zoom to the polygon's bounds
        m.fit_bounds(polygon.get_bounds())

        # Display the map in Streamlit
        st_folium(m, width=700, height=500)


        # Streamlit app interface
        st.title("Real Estate Sales Trend Analysis")

        # User input for geo_id
        

    else:
        # Provide guidance if no input is given
        st.write("Please enter an APN and FIP")
