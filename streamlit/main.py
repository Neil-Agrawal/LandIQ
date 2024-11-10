import streamlit as st
import importlib

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Crime", "Econmic Stability", "Transportation Accessibility", "Financial Overview","Zoning Regulations", "Environmental Overview"])

# Dynamically load pages based on selection
if page == "Home":
    module = importlib.import_module("home")
elif page == "Crime":
    module = importlib.import_module("crime")
elif page == "Econmic Stability":
    module = importlib.import_module("economic_stability")
elif page == "Transportation Accessibility":
    module = importlib.import_module("transpaccess")
elif page == "Financial Overview":
    module = importlib.import_module("financial")
elif page == "Zoning Regulations":
    module = importlib.import_module("zone")
elif page == "Environmental Overview":
    module = importlib.import_module("envi")

# Run the selected page's code
if module:
    module.run()  # Assumes each page file has a `run` function
