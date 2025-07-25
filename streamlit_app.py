import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Location Finder", layout="centered")

st.title("📍 Where Was This Taken?")
st.markdown("Use clues to help identify a location you've visited.")

# --- Inputs ---
city = st.text_input("Nearest city or town", placeholder="e.g. Wichita, KS")
road = st.text_input("Known road or highway", placeholder="Optional")
keywords = st.text_area("Describe what you remember", placeholder="e.g. Emprise Bank, Taco Bell, Ace Hardware...")

if st.button("Search"):
    if not city and not keywords:
        st.warning("Please provide at least a city or some description.")
    else:
        with st.spinner("Searching..."):
            # Build the search query
            query = f"{keywords} near {city}"
            if road:
                query = f"{keywords} near {road}, {city}"

            # Format query for URL
            encoded_query = urllib.parse.quote_plus(query)

            # Google Places Text Search API
            api_key = st.secrets["google_api_key"]
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_query}&key={api_key}"

            response = requests.get(url)
            data = response.json()

            results = data.get("results", [])

            if not results:
                st.error("No places found based on the information you provided.")
            else:
                st.success(f"Found {len(results)} matching place(s):")
                for place in results[:10]:
                    name = place.get("name")
                    address = place.get("formatted_address")
                    location = place.get("geometry", {}).get("location", {})
                    lat = location.get("lat")
                    lng = location.get("lng")
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

                    st.markdown(f"""
                    **{name}**  
                    📍 {address}  
                    🌐 [View on Google Maps]({gmaps_url})
                    """)
