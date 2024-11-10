import requests

def get_sales_trend_2022(geo_id):
    url = "https://api.gateway.attomdata.com/v4/transaction/salestrend"
    interval="yearly"
    start_year=2018
    end_year=2022,
    api_key="2b1e86b638620bf2404521e6e9e1b19e"
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

            # Display the CMA for 2022
            print("Comparative Market Analysis (CMA) for 2022")
            print("=========================================")
            print(f"Home Sale Count: {home_sale_count}")
            print(f"Average Sale Price: ${avg_sale_price:,.2f}")

            # User input for number of houses they plan to build
            num_houses_to_build = int(input("Enter the number of houses you plan to build: "))
            fmv = num_houses_to_build * avg_sale_price

            # Display the Fair Market Value
            print("\nEstimated Fair Market Value (FMV) of the Land")
            print("=========================================")
            print(f"Number of Houses Planned: {num_houses_to_build}")
            print(f"Total FMV: ${fmv:,.2f}")
            
        except (KeyError, StopIteration):
            print("Sales trend data for 2022 not found in response.")
    else:
        print(f"Error: {response.status_code}")
# Example usage
# api_key = "2b1e86b638620bf2404521e6e9e1b19e"
geo_id = "6f61bd55d6f16014cae7f1c685cffbbc"
interval = "yearly"
start_year = 2018
end_year = 2022

get_sales_trend_2022(geo_id, interval, start_year, end_year)