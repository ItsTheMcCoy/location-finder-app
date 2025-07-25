import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Location Finder", layout="centered")
st.title("📍 Where Was This Taken?")
st.markdown("Use clues to help identify a location you've visited.")

city = st.text_input("Nearest city or town", placeholder="e.g. Wichita, KS")
road = st.text_input("Known road or highway", placeholder="Optional")
keywords = st.text_area("Describe what you remember", placeholder="e.g. Emprise Bank, Taco Bell, Ace Hardware...")

if st.button("Search"):
    if not city and not keywords:
        st.warning("Please provide at least a city or some description.")
    else:
        st.info("Running multiple searches based on your memory clues...")

        api_key = st.secrets["google_api_key"]
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

        matches = []

        for keyword in keyword_list:
            search_term = f"{keyword} near {road}, {city}" if road else f"{keyword} near {city}"
            encoded_query = urllib.parse.quote_plus(search_term)
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_query}&key={api_key}"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for place in data.get("results", [])[:3]:  # Limit to top 3 per term
                    name = place.get("name")
                    address = place.get("formatted_address")
                    location = place.get("geometry", {}).get("location", {})
                    lat, lng = location.get("lat"), location.get("lng")
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

                    matches.append((name, address, gmaps_url))

        if not matches:
            st.error("No places found based on the individual clues provided.")
        else:
            st.success(f"Found {len(matches)} matching places:")
            for name, address, gmaps_url in matches:
                st.markdown(f"""
                **{name}**  
                📍 {address}  
                🌐 [View on Google Maps]({gmaps_url})
                """)
