import streamlit as st
import folium
from streamlit_folium import st_folium

# Import Google Maps API key
try:
    from dashboard_config import GOOGLE_MAPS_API_KEY
    st.write(f"Google Maps API Key loaded: {GOOGLE_MAPS_API_KEY[:10]}..." if GOOGLE_MAPS_API_KEY else "No API Key found")
except ImportError:
    GOOGLE_MAPS_API_KEY = None
    st.write("Could not import dashboard_config")

st.title("Google Maps API Test")

# Create a simple map to test Google Maps integration
m = folium.Map(
    location=[-1.2921, 36.8219],  # Nairobi
    zoom_start=10,
    tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
)

# Add Google Maps tile layer if API key is available
if GOOGLE_MAPS_API_KEY:
    try:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st.success("Google Maps layers added successfully!")
    except Exception as e:
        st.error(f"Error adding Google Maps layers: {e}")
else:
    st.warning("No Google Maps API key found, using OpenStreetMap")

# Display map
st_folium(m, width=700, height=500)