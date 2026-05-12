import streamlit as st
import requests

st.set_page_config(page_title="Real Estate AI", page_icon="🏠")

st.title("🏠 Property Valuation Dashboard")

with st.sidebar:
    st.header("Input Parameters")
    area = st.number_input("Area (Sq Ft)", min_value=100, value=1200)
    beds = st.number_input("Bedrooms", 1, 10, 2)
    baths = st.number_input("Bathrooms", 1, 10, 2)
    age = st.number_input("Age of Property", 0, 100, 5)
    location = st.selectbox("Location", ["Downtown", "Suburb", "Rural", "Uptown"])
    p_type = st.selectbox("Property Type", ["Apartment", "House", "Condo", "Villa"])

if st.button("Get Price Estimate"):
    # The keys here MUST match the Pydantic model in FastAPI
    payload = {
        "Area": area,
        "Bedrooms": beds,
        "Bathrooms": baths,
        "Age": age,
        "Location": location,
        "Property_Type": p_type
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        prediction = response.json()["Price_Estimate"]
        st.balloons()
        st.success(f"### Estimated Market Price: ${prediction:,.2f}")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
