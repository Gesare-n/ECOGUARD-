import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime
import os
import zipfile
import io
import base64

# Import Google Maps API key
try:
    from dashboard_config import GOOGLE_MAPS_API_KEY
except ImportError:
    GOOGLE_MAPS_API_KEY = None

# Set page config
st.set_page_config(
    page_title="EcoGuard - Kenya Google Earth Export",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 EcoGuard - Kenya Forest Data for Google Earth")
st.markdown("### Export KML files for viewing in Google Earth")

# Load Kenya forest data
@st.cache_data
def load_forest_data():
    """Load Kenya forest data from CSV file"""
    if os.path.exists("kenya_forest_locations.csv"):
        return pd.read_csv("kenya_forest_locations.csv")
    else:
        # Fallback to hardcoded data
        forest_data = {
            "name": ["Karura Forest", "Uhuru Park", "Ngong Forest", "Aberdare Forest", "Mt. Kenya Forest", "Arboretum Forest", "Kakamega Forest", "Mau Forest", "Chyulu Hills Forest", "Taita Hills Forest"],
            "lat": [-1.2723, -1.3037, -1.3500, -0.4500, -0.2500, -0.5300, 0.3000, -0.5000, -2.5000, -3.5000],
            "lng": [36.8080, 36.8166, 36.7000, 36.5000, 37.7500, 36.5300, 34.7500, 35.5000, 38.0000, 38.5000],
            "area_km2": [17.5, 0.6, 20.0, 200.0, 150.0, 5.0, 70.0, 400.0, 150.0, 25.0],
            "type": ["Urban Forest", "Urban Park", "Indigenous Forest", "Mountain Forest", "Mountain Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest"]
        }
        return pd.DataFrame(forest_data)

# Load deforestation risk model
@st.cache_data
def load_risk_data():
    """Load deforestation risk model data"""
    if os.path.exists("deforestation_risk_model.csv"):
        return pd.read_csv("deforestation_risk_model.csv")
    else:
        # Fallback to hardcoded data
        risk_data = {
            "forest": ["Karura Forest", "Uhuru Park", "Ngong Forest", "Aberdare Forest", "Mt. Kenya Forest", "Kakamega Forest"],
            "urban_proximity": [0.9, 1.0, 0.7, 0.2, 0.3, 0.4],
            "accessibility": [0.8, 1.0, 0.7, 0.4, 0.5, 0.6],
            "historical_loss": [0.3, 0.8, 0.5, 0.2, 0.1, 0.6],
            "risk_score": [0.67, 0.93, 0.63, 0.27, 0.30, 0.53]
        }
        return pd.DataFrame(risk_data)

# Function to create KML content
def create_kml_content(name, placemarks):
    """Create KML content for export"""
    kml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>{}</name>
<description>EcoGuard - Kenya Forest Data</description>
<Style id="forestStyle">
    <IconStyle>
        <color>ff00ff00</color>
        <scale>1.0</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="reforestationStyle">
    <IconStyle>
        <color>ff00ffff</color>
        <scale>1.0</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="deforestationStyle">
    <IconStyle>
        <color>ff0000ff</color>
        <scale>1.0</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="highRiskStyle">
    <IconStyle>
        <color>ff0000ff</color>
        <scale>1.2</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="mediumRiskStyle">
    <IconStyle>
        <color>ff00a5ff</color>
        <scale>1.1</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/orange-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="lowRiskStyle">
    <IconStyle>
        <color>ff00ff00</color>
        <scale>1.0</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png</href>
        </Icon>
    </IconStyle>
</Style>
'''.format(name)
    
    kml_placemarks = ""
    for placemark in placemarks:
        kml_placemarks += '''
<Placemark>
    <name>{}</name>
    <description>{}</description>
    <styleUrl>{}</styleUrl>
    <Point>
        <coordinates>{},{},0</coordinates>
    </Point>
</Placemark>'''.format(
            placemark['name'],
            placemark['description'],
            placemark['style'],
            placemark['lng'],
            placemark['lat']
        )
    
    kml_footer = '''
</Document>
</kml>'''
    
    return kml_header + kml_placemarks + kml_footer

# Load data
forest_data = load_forest_data()
risk_data = load_risk_data()

# Convert to dictionary for easier access
FOREST_LOCATIONS = {}
for _, row in forest_data.iterrows():
    FOREST_LOCATIONS[row['name']] = {
        "lat": row['lat'],
        "lng": row['lng'],
        "area_km2": row['area_km2'],
        "type": row['type']
    }

# Create tabs for different exports
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌳 All Forests", 
    "🌱 Reforestation Areas", 
    "🔥 Deforestation Areas", 
    "📡 Sensor Priorities",
    "🌿 Nursery Monitoring",
    "📦 Download All"
])

with tab1:
    st.subheader("All Forests in Kenya")
    
    # Prepare placemarks for KML
    placemarks = []
    for forest, coords in FOREST_LOCATIONS.items():
        description = f"Area: {coords['area_km2']} km²\nType: {coords['type']}"
        placemarks.append({
            'name': forest,
            'lat': coords['lat'],
            'lng': coords['lng'],
            'description': description,
            'style': '#forestStyle'
        })
    
    # Create KML content
    kml_content = create_kml_content("Kenya Forests", placemarks)
    
    # Display map with Google Maps
    m1 = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
    )
    
    # Add Google Maps tile layer if API key is available
    if GOOGLE_MAPS_API_KEY:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m1)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m1)
        
        folium.LayerControl().add_to(m1)

    # Add forest markers
    for forest, coords in FOREST_LOCATIONS.items():
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²<br>Type: {coords['type']}",
            tooltip=forest,
            icon=folium.Icon(color='green', icon="tree", prefix='fa')
        ).add_to(m1)
    
    st_folium(m1, width=700, height=500)
    
    # Download button
    b64 = base64.b64encode(kml_content.encode()).decode()
    href = f'<a href="data:application/vnd.google-earth.kml+xml;base64,{b64}" download="kenya_forests.kml">Download KML File</a>'
    st.markdown(href, unsafe_allow_html=True)

with tab2:
    st.subheader("Reforestation Areas")
    
    # Mock reforestation data
    reforestation_data = [
        {"area": "Karura Forest - Northern Section", "lat": -1.2650, "lng": 36.8100, "hectares": 15, "trees_planted": 2500, "planting_date": "2024-01-15"},
        {"area": "Ngong Forest - Eastern Edge", "lat": -1.3450, "lng": 36.7100, "hectares": 8, "trees_planted": 1200, "planting_date": "2024-02-20"},
        {"area": "Arboretum Forest - Southern Zone", "lat": -0.5400, "lng": 36.5200, "hectares": 3, "trees_planted": 800, "planting_date": "2024-03-10"},
        {"area": "Mau Forest - Restoration Zone A", "lat": -0.4800, "lng": 35.4800, "hectares": 45, "trees_planted": 6500, "planting_date": "2024-01-30"}
    ]
    
    # Prepare placemarks for KML
    placemarks = []
    for area in reforestation_data:
        description = f"Hectares: {area['hectares']}\nTrees Planted: {area['trees_planted']:,}\nPlanting Date: {area['planting_date']}"
        placemarks.append({
            'name': area['area'],
            'lat': area['lat'],
            'lng': area['lng'],
            'description': description,
            'style': '#reforestationStyle'
        })
    
    # Create KML content
    kml_content = create_kml_content("Reforestation Areas", placemarks)
    
    # Display map with Google Maps
    m2 = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
    )
    
    # Add Google Maps tile layer if API key is available
    if GOOGLE_MAPS_API_KEY:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m2)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m2)
        
        folium.LayerControl().add_to(m2)

    # Add reforestation markers
    for area in reforestation_data:
        folium.CircleMarker(
            location=[area["lat"], area["lng"]],
            radius=10,
            popup=f"<b>{area['area']}</b><br>Hectares: {area['hectares']}<br>Trees Planted: {area['trees_planted']:,}<br>Planting Date: {area['planting_date']}",
            tooltip=f"{area['area']} - {area['trees_planted']:,} trees",
            color='green',
            fill=True,
            fillColor='green'
        ).add_to(m2)
    
    st_folium(m2, width=700, height=500)
    
    # Download button
    b64 = base64.b64encode(kml_content.encode()).decode()
    href = f'<a href="data:application/vnd.google-earth.kml+xml;base64,{b64}" download="reforestation_areas.kml">Download KML File</a>'
    st.markdown(href, unsafe_allow_html=True)

with tab3:
    st.subheader("Deforestation Areas")
    
    # Mock deforestation data
    deforestation_data = [
        {"area": "Mau Forest - Western Section", "lat": -0.5200, "lng": 35.4500, "hectares_lost": 120, "year": 2023, "cause": "Agricultural Expansion"},
        {"area": "Kakamega Forest - Northern Edge", "lat": 0.3200, "lng": 34.7300, "hectares_lost": 45, "year": 2023, "cause": "Illegal Logging"},
        {"area": "Taita Hills Forest", "lat": -3.4800, "lng": 38.4800, "hectares_lost": 18, "year": 2023, "cause": "Charcoal Production"},
        {"area": "Chyulu Hills Forest - Southern Zone", "lat": -2.5200, "lng": 37.9800, "hectares_lost": 32, "year": 2023, "cause": "Settlements"}
    ]
    
    # Prepare placemarks for KML
    placemarks = []
    for area in deforestation_data:
        description = f"Hectares Lost: {area['hectares_lost']}\nYear: {area['year']}\nCause: {area['cause']}"
        placemarks.append({
            'name': area['area'],
            'lat': area['lat'],
            'lng': area['lng'],
            'description': description,
            'style': '#deforestationStyle'
        })
    
    # Create KML content
    kml_content = create_kml_content("Deforestation Areas", placemarks)
    
    # Display map with Google Maps
    m3 = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
    )
    
    # Add Google Maps tile layer if API key is available
    if GOOGLE_MAPS_API_KEY:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m3)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m3)
        
        folium.LayerControl().add_to(m3)

    # Add deforestation markers
    for area in deforestation_data:
        folium.CircleMarker(
            location=[area["lat"], area["lng"]],
            radius=12,
            popup=f"<b>{area['area']}</b><br>Hectares Lost: {area['hectares_lost']}<br>Year: {area['year']}<br>Cause: {area['cause']}",
            tooltip=f"{area['area']} - {area['hectares_lost']} ha lost",
            color='red',
            fill=True,
            fillColor='red'
        ).add_to(m3)
    
    st_folium(m3, width=700, height=500)
    
    # Download button
    b64 = base64.b64encode(kml_content.encode()).decode()
    href = f'<a href="data:application/vnd.google-earth.kml+xml;base64,{b64}" download="deforestation_areas.kml">Download KML File</a>'
    st.markdown(href, unsafe_allow_html=True)

with tab4:
    st.subheader("Sensor Priority Areas")
    
    # Prepare placemarks for KML with risk-based styling
    placemarks = []
    for forest, coords in FOREST_LOCATIONS.items():
        # Get risk score for this forest
        risk_score = 0.5  # Default risk score
        if forest in risk_data["forest"].values:
            risk_score = risk_data[risk_data["forest"] == forest]["risk_score"].iloc[0]
        
        # Style based on risk score
        if risk_score >= 0.7:
            style = '#highRiskStyle'
            priority = "High"
        elif risk_score >= 0.4:
            style = '#mediumRiskStyle'
            priority = "Medium"
        else:
            style = '#lowRiskStyle'
            priority = "Low"
        
        # Recommended sensors based on area and risk
        recommended_sensors = max(1, int(coords["area_km2"] / 50 * (risk_score * 2)))
        
        description = f"Area: {coords['area_km2']} km²\nRisk Score: {risk_score:.2f}\nPriority: {priority}\nRecommended Sensors: {recommended_sensors}"
        
        placemarks.append({
            'name': f"{forest} ({priority} Priority)",
            'lat': coords['lat'],
            'lng': coords['lng'],
            'description': description,
            'style': style
        })
    
    # Create KML content
    kml_content = create_kml_content("Sensor Priority Areas", placemarks)
    
    # Display map with Google Maps
    m4 = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
    )
    
    # Add Google Maps tile layer if API key is available
    if GOOGLE_MAPS_API_KEY:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m4)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m4)
        
        folium.LayerControl().add_to(m4)

    # Add forest markers with risk-based coloring
    for forest, coords in FOREST_LOCATIONS.items():
        # Get risk score for this forest
        risk_score = 0.5  # Default risk score
        if forest in risk_data["forest"].values:
            risk_score = risk_data[risk_data["forest"] == forest]["risk_score"].iloc[0]
        
        # Color based on risk score
        if risk_score >= 0.7:
            color = "red"
            priority = "High"
        elif risk_score >= 0.4:
            color = "orange"
            priority = "Medium"
        else:
            color = "green"
            priority = "Low"
        
        # Recommended sensors based on area and risk
        recommended_sensors = max(1, int(coords["area_km2"] / 50 * (risk_score * 2)))
        
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²<br>Risk Score: {risk_score:.2f}<br>Priority: {priority}<br>Recommended Sensors: {recommended_sensors}",
            tooltip=f"{forest} - {priority} Priority",
            icon=folium.Icon(color=color, icon="exclamation-sign" if priority == "High" else "info-sign", prefix='glyphicon')
        ).add_to(m4)
    
    st_folium(m4, width=700, height=500)
    
    # Download button
    b64 = base64.b64encode(kml_content.encode()).decode()
    href = f'<a href="data:application/vnd.google-earth.kml+xml;base64,{b64}" download="sensor_priorities.kml">Download KML File</a>'
    st.markdown(href, unsafe_allow_html=True)

with tab5:
    st.subheader("Nursery Monitoring")
    
    # Mock nursery data
    nursery_data = [
        {"name": "Karura Forest Nursery", "lat": -1.2700, "lng": 36.8100, "seedlings": 5000, "species": "Indigenous Trees", "status": "Healthy", "last_review": "2024-05-15", "next_review": "2024-06-15"},
        {"name": "Ngong Forest Seed Bank", "lat": -1.3400, "lng": 36.6900, "seedlings": 12000, "species": "Acacia, Croton", "status": "Needs Attention", "last_review": "2024-04-22", "next_review": "2024-05-22"},
        {"name": "Aberdare Reforestation Hub", "lat": -0.4400, "lng": 36.4900, "seedlings": 8500, "species": "Oak, Cedar", "status": "Healthy", "last_review": "2024-05-10", "next_review": "2024-06-10"},
        {"name": "Kakamega Tree Farm", "lat": 0.2900, "lng": 34.7400, "seedlings": 6200, "species": "Indigenous Shade Trees", "status": "Excellent", "last_review": "2024-05-18", "next_review": "2024-06-18"},
        {"name": "Mau Forest Greenhouse", "lat": -0.4900, "lng": 35.4900, "seedlings": 15000, "species": "Various Native Species", "status": "Critical", "last_review": "2024-03-30", "next_review": "2024-05-30"}
    ]
    
    # Prepare placemarks for KML with status-based styling
    placemarks = []
    for nursery in nursery_data:
        description = f"Seedlings: {nursery['seedlings']:,}\nSpecies: {nursery['species']}\nStatus: {nursery['status']}\nLast Review: {nursery['last_review']}\nNext Review: {nursery['next_review']}"
        
        # Style based on status
        if nursery["status"] == "Excellent":
            style = '#lowRiskStyle'
        elif nursery["status"] == "Healthy":
            style = '#lowRiskStyle'
        elif nursery["status"] == "Needs Attention":
            style = '#mediumRiskStyle'
        else:  # Critical
            style = '#highRiskStyle'
        
        placemarks.append({
            'name': f"{nursery['name']} ({nursery['status']})",
            'lat': nursery['lat'],
            'lng': nursery['lng'],
            'description': description,
            'style': style
        })
    
    # Create KML content
    kml_content = create_kml_content("Nursery Monitoring", placemarks)
    
    # Display map
    m5 = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap' if not GOOGLE_MAPS_API_KEY else None
    )
    
    # Add Google Maps tile layer if API key is available
    if GOOGLE_MAPS_API_KEY:
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(m5)
        
        # Add satellite view as well
        folium.TileLayer(
            tiles=f'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key={GOOGLE_MAPS_API_KEY}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m5)
        
        folium.LayerControl().add_to(m5)
    
    # Add nursery markers with color coding based on status
    for nursery in nursery_data:
        if nursery["status"] == "Excellent":
            color = "green"
        elif nursery["status"] == "Healthy":
            color = "lightgreen"
        elif nursery["status"] == "Needs Attention":
            color = "orange"
        else:  # Critical
            color = "red"
        
        folium.Marker(
            location=[nursery["lat"], nursery["lng"]],
            popup=f"<b>{nursery['name']}</b><br>Seedlings: {nursery['seedlings']:,}<br>Species: {nursery['species']}<br>Status: {nursery['status']}<br>Last Review: {nursery['last_review']}<br>Next Review: {nursery['next_review']}",
            tooltip=f"{nursery['name']} - {nursery['status']}",
            icon=folium.Icon(color=color, icon="leaf", prefix='fa')
        ).add_to(m5)
    
    st_folium(m5, width=700, height=500)
    
    # Download button
    b64 = base64.b64encode(kml_content.encode()).decode()
    href = f'<a href="data:application/vnd.google-earth.kml+xml;base64,{b64}" download="nursery_monitoring.kml">Download KML File</a>'
    st.markdown(href, unsafe_allow_html=True)

with tab6:
    st.subheader("Download All KML Files")
    st.markdown("Download a ZIP file containing all KML files for use in Google Earth:")
    
    # Create ZIP file with all KML files
    def create_zip_file():
        # Create in-memory ZIP file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add all KML files to ZIP
            # Forests KML
            forest_placemarks = []
            for forest, coords in FOREST_LOCATIONS.items():
                description = f"Area: {coords['area_km2']} km²\nType: {coords['type']}"
                forest_placemarks.append({
                    'name': forest,
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'description': description,
                    'style': '#forestStyle'
                })
            forests_kml = create_kml_content("Kenya Forests", forest_placemarks)
            zip_file.writestr("kenya_forests.kml", forests_kml)
            
            # Reforestation KML
            reforestation_data = [
                {"area": "Karura Forest - Northern Section", "lat": -1.2650, "lng": 36.8100, "hectares": 15, "trees_planted": 2500, "planting_date": "2024-01-15"},
                {"area": "Ngong Forest - Eastern Edge", "lat": -1.3450, "lng": 36.7100, "hectares": 8, "trees_planted": 1200, "planting_date": "2024-02-20"},
                {"area": "Arboretum Forest - Southern Zone", "lat": -0.5400, "lng": 36.5200, "hectares": 3, "trees_planted": 800, "planting_date": "2024-03-10"},
                {"area": "Mau Forest - Restoration Zone A", "lat": -0.4800, "lng": 35.4800, "hectares": 45, "trees_planted": 6500, "planting_date": "2024-01-30"}
            ]
            
            reforestation_placemarks = []
            for area in reforestation_data:
                description = f"Hectares: {area['hectares']}\nTrees Planted: {area['trees_planted']:,}\nPlanting Date: {area['planting_date']}"
                reforestation_placemarks.append({
                    'name': area['area'],
                    'lat': area['lat'],
                    'lng': area['lng'],
                    'description': description,
                    'style': '#reforestationStyle'
                })
            reforestation_kml = create_kml_content("Reforestation Areas", reforestation_placemarks)
            zip_file.writestr("reforestation_areas.kml", reforestation_kml)
            
            # Deforestation KML
            deforestation_data = [
                {"area": "Mau Forest - Western Section", "lat": -0.5200, "lng": 35.4500, "hectares_lost": 120, "year": 2023, "cause": "Agricultural Expansion"},
                {"area": "Kakamega Forest - Northern Edge", "lat": 0.3200, "lng": 34.7300, "hectares_lost": 45, "year": 2023, "cause": "Illegal Logging"},
                {"area": "Taita Hills Forest", "lat": -3.4800, "lng": 38.4800, "hectares_lost": 18, "year": 2023, "cause": "Charcoal Production"},
                {"area": "Chyulu Hills Forest - Southern Zone", "lat": -2.5200, "lng": 37.9800, "hectares_lost": 32, "year": 2023, "cause": "Settlements"}
            ]
            
            deforestation_placemarks = []
            for area in deforestation_data:
                description = f"Hectares Lost: {area['hectares_lost']}\nYear: {area['year']}\nCause: {area['cause']}"
                deforestation_placemarks.append({
                    'name': area['area'],
                    'lat': area['lat'],
                    'lng': area['lng'],
                    'description': description,
                    'style': '#deforestationStyle'
                })
            deforestation_kml = create_kml_content("Deforestation Areas", deforestation_placemarks)
            zip_file.writestr("deforestation_areas.kml", deforestation_kml)
            
            # Sensor Priorities KML
            sensor_placemarks = []
            for forest, coords in FOREST_LOCATIONS.items():
                # Get risk score for this forest
                risk_score = 0.5  # Default risk score
                if forest in risk_data["forest"].values:
                    risk_score = risk_data[risk_data["forest"] == forest]["risk_score"].iloc[0]
                
                # Style based on risk score
                if risk_score >= 0.7:
                    style = '#highRiskStyle'
                    priority = "High"
                elif risk_score >= 0.4:
                    style = '#mediumRiskStyle'
                    priority = "Medium"
                else:
                    style = '#lowRiskStyle'
                    priority = "Low"
                
                # Recommended sensors based on area and risk
                recommended_sensors = max(1, int(coords["area_km2"] / 50 * (risk_score * 2)))
                
                description = f"Area: {coords['area_km2']} km²\nRisk Score: {risk_score:.2f}\nPriority: {priority}\nRecommended Sensors: {recommended_sensors}"
                
                sensor_placemarks.append({
                    'name': f"{forest} ({priority} Priority)",
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'description': description,
                    'style': style
                })
            sensors_kml = create_kml_content("Sensor Priority Areas", sensor_placemarks)
            zip_file.writestr("sensor_priorities.kml", sensors_kml)
            
            # Nursery Monitoring KML
            nursery_data = [
                {"name": "Karura Forest Nursery", "lat": -1.2700, "lng": 36.8100, "seedlings": 5000, "species": "Indigenous Trees", "status": "Healthy", "last_review": "2024-05-15", "next_review": "2024-06-15"},
                {"name": "Ngong Forest Seed Bank", "lat": -1.3400, "lng": 36.6900, "seedlings": 12000, "species": "Acacia, Croton", "status": "Needs Attention", "last_review": "2024-04-22", "next_review": "2024-05-22"},
                {"name": "Aberdare Reforestation Hub", "lat": -0.4400, "lng": 36.4900, "seedlings": 8500, "species": "Oak, Cedar", "status": "Healthy", "last_review": "2024-05-10", "next_review": "2024-06-10"},
                {"name": "Kakamega Tree Farm", "lat": 0.2900, "lng": 34.7400, "seedlings": 6200, "species": "Indigenous Shade Trees", "status": "Excellent", "last_review": "2024-05-18", "next_review": "2024-06-18"},
                {"name": "Mau Forest Greenhouse", "lat": -0.4900, "lng": 35.4900, "seedlings": 15000, "species": "Various Native Species", "status": "Critical", "last_review": "2024-03-30", "next_review": "2024-05-30"}
            ]
            
            nursery_placemarks = []
            for nursery in nursery_data:
                description = f"Seedlings: {nursery['seedlings']:,}\nSpecies: {nursery['species']}\nStatus: {nursery['status']}\nLast Review: {nursery['last_review']}\nNext Review: {nursery['next_review']}"
                
                # Style based on status
                if nursery["status"] == "Excellent":
                    style = '#lowRiskStyle'
                elif nursery["status"] == "Healthy":
                    style = '#lowRiskStyle'
                elif nursery["status"] == "Needs Attention":
                    style = '#mediumRiskStyle'
                else:  # Critical
                    style = '#highRiskStyle'
                
                nursery_placemarks.append({
                    'name': f"{nursery['name']} ({nursery['status']})",
                    'lat': nursery['lat'],
                    'lng': nursery['lng'],
                    'description': description,
                    'style': style
                })
            nursery_kml = create_kml_content("Nursery Monitoring", nursery_placemarks)
            zip_file.writestr("nursery_monitoring.kml", nursery_kml)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    # Download button for ZIP file
    zip_data = create_zip_file()
    b64 = base64.b64encode(zip_data).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="kenya_forest_data_all.kml.zip">Download All KML Files (ZIP)</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### How to Use in Google Earth:")
    st.markdown("""
    1. Download the KML file(s) using the buttons above
    2. Open Google Earth Pro (free desktop application)
    3. Click "File" → "Open" and select the downloaded KML file
    4. The data will appear in the "Places" panel and on the map
    5. You can turn layers on/off using the checkboxes in the Places panel
    """)

# Footer
st.markdown("---")
st.markdown("🌍 EcoGuard - Kenya Forest Intelligence for Google Earth")
st.markdown("Exported data includes forests, reforestation areas, deforestation zones, and sensor priorities")