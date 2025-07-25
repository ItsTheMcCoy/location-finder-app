import streamlit as st

st.title("Where Was This Taken?")
city = st.text_input("Nearest city or town")
road = st.text_input("Known road or highway")
keywords = st.text_area("Describe what you remember")

if st.button("Search"):
    st.write("Searching...")
    st.write(f"City: {city}, Road: {road}, Clues: {keywords}")
