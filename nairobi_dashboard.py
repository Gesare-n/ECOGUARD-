"""
Acoustic Guardian - Nairobi Forest Conservation Dashboard

This dashboard focuses on forest conservation efforts in Nairobi and surrounding areas,
including Karura Forest and other areas affected by deforestation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Acoustic Guardian - Nairobi Forests",
    page_icon="🌳",
    layout="wide"
)

# Nairobi forest locations with actual coordinates
FOREST_LOCATIONS = {
    "Karura Forest": {"lat": -1.2723, "lng": 36.8080, "area_km2": 17.5},
    "Uhuru Park": {"lat": -1.3037, "lng": 36.8166, "area_km2": 0.6},
    "Central Park": {"lat": -1.2864, "lng": 36.8172, "area_km2": 0.5},
    "Jeevanjee Gardens": {"lat": -1.2833, "lng": 36.8222, "area_km2": 0.2},
    "Ngong Forest": {"lat": -1.3500, "lng": 36.7000, "area_km2": 20.0},
    "Aberdare Forest": {"lat": -0.4500, "lng": 36.5000, "area_km2": 200.0}
}

# Deforestation data for Nairobi region (mock data)
DEFORESTATION_DATA = [
    {"year": 2015, "area_hectares": 1200, "location": "Karura Forest", "cause": "Urban Expansion"},
    {"year": 2016, "area_hectares": 950, "location": "Karura Forest", "cause": "Illegal Logging"},
    {"year": 2017, "area_hectares": 780, "location": "Karura Forest", "cause": "Agriculture"},
    {"year": 2018, "area_hectares": 620, "location": "Karura Forest", "cause": "Infrastructure"},
    {"year": 2019, "area_hectares": 510, "location": "Karura Forest", "cause": "Urban Expansion"},
    {"year": 2020, "area_hectares": 430, "location": "Karura Forest", "cause": "Illegal Logging"},
    {"year": 2021, "area_hectares": 320, "location": "Karura Forest", "cause": "Agriculture"},
    {"year": 2022, "area_hectares": 210, "location": "Karura Forest", "cause": "Conservation Efforts"},
    {"year": 2023, "area_hectares": 150, "location": "Karura Forest", "cause": "Conservation Efforts"},
    {"year": 2024, "area_hectares": 90, "location": "Karura Forest", "cause": "Conservation Efforts"},
    {"year": 2015, "area_hectares": 800, "location": "Ngong Forest", "cause": "Urban Expansion"},
    {"year": 2016, "area_hectares": 720, "location": "Ngong Forest", "cause": "Charcoal Production"},
    {"year": 2017, "area_hectares": 650, "location": "Ngong Forest", "cause": "Agriculture"},
    {"year": 2018, "area_hectares": 580, "location": "Ngong Forest", "cause": "Settlements"},
    {"year": 2019, "area_hectares": 490, "location": "Ngong Forest", "cause": "Urban Expansion"},
    {"year": 2020, "area_hectares": 410, "location": "Ngong Forest", "cause": "Charcoal Production"},
    {"year": 2021, "area_hectares": 330, "location": "Ngong Forest", "cause": "Agriculture"},
    {"year": 2022, "area_hectares": 260, "location": "Ngong Forest", "cause": "Conservation Efforts"},
    {"year": 2023, "area_hectares": 180, "location": "Ngong Forest", "cause": "Conservation Efforts"},
    {"year": 2024, "area_hectares": 120, "location": "Ngong Forest", "cause": "Conservation Efforts"}
]

# Mock sensor data for demonstration
def generate_sensor_data():
    # Set seed for consistent data generation
    random.seed(42)
    sensors = []
    for i, (forest, coords) in enumerate(FOREST_LOCATIONS.items()):
        sensor = {
            "id": f"AG-{str(i+1).zfill(3)}",
            "forest": forest,
            "lat": coords["lat"],
            "lng": coords["lng"],
            "status": random.choice(["🟢 Active", "🟡 Warning", "🔴 Offline"]),
            "battery": round(random.uniform(70, 100), 1),
            "signal": random.randint(-80, -50),
            "last_detection": random.choice([None, "Chainsaw", "Vehicle", "None"]),
            "detections_today": random.randint(0, 5)
        }
        sensors.append(sensor)
    return sensors

# Create sidebar
st.sidebar.title("🌳 Acoustic Guardian")
st.sidebar.markdown("### Nairobi Forest Conservation")

# Date range selector
st.sidebar.subheader("📅 Date Range")
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Forest selector
st.sidebar.subheader("Forest Selection")
selected_forests = st.sidebar.multiselect(
    "Select Forests",
    list(FOREST_LOCATIONS.keys()),
    default=["Karura Forest", "Ngong Forest"]
)

# Sensor status filter
st.sidebar.subheader("📡 Sensor Status")
status_filter = st.sidebar.radio(
    "Filter by Status",
    ["All", "Active", "Warning", "Offline"],
    index=0
)

# Main dashboard
st.title("🌳 Acoustic Guardian - Nairobi Forest Conservation Dashboard")
st.markdown("### Monitoring and protecting Nairobi's precious forest ecosystems")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active Sensors", 
        value="6", 
        delta="2 new this month"
    )

with col2:
    st.metric(
        label="Detections Today", 
        value="12",
        delta="↓ 3 from yesterday"
    )

with col3:
    st.metric(
        label="Protected Area", 
        value="238.8 km²",
        delta="↑ 12 km² conserved"
    )

with col4:
    st.metric(
        label="Deforestation (2024)", 
        value="210 ha",
        delta="↓ 45% from 2020"
    )

# Map and sensor status
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📍 Forest Locations & Sensor Network")
    
    # Create map centered on Nairobi
    m = folium.Map(
        location=[-1.2921, 36.8219],  # Center of Nairobi
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add forest markers
    for forest, coords in FOREST_LOCATIONS.items():
        color = "green" if forest in selected_forests else "blue"
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²",
            tooltip=forest,
            icon=folium.Icon(color=color, icon="tree", prefix='fa')
        ).add_to(m)
        
        # Add sensor markers
        # Simulate sensors around each forest
        for i in range(3):
            sensor_lat = coords["lat"] + random.uniform(-0.01, 0.01)
            sensor_lng = coords["lng"] + random.uniform(-0.01, 0.01)
            
            # Randomly determine if this sensor detected something
            detection = random.choice([True, False, False])  # 33% chance of detection
            
            if detection:
                folium.CircleMarker(
                    location=[sensor_lat, sensor_lng],
                    radius=8,
                    popup=f"Sensor AG-{random.randint(100, 999)}<br>Detection: Chainsaw",
                    color='red',
                    fill=True,
                    fillColor='red'
                ).add_to(m)
            else:
                folium.CircleMarker(
                    location=[sensor_lat, sensor_lng],
                    radius=6,
                    popup=f"Sensor AG-{random.randint(100, 999)}<br>Status: Active",
                    color='green',
                    fill=True,
                    fillColor='green'
                ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("📡 Sensor Status")
    
    # Generate sensor data
    sensors = generate_sensor_data()
    
    # Filter sensors based on sidebar selection
    if status_filter != "All":
        status_map = {"Active": "🟢 Active", "Warning": "🟡 Warning", "Offline": "🔴 Offline"}
        sensors = [s for s in sensors if s["status"] == status_map[status_filter]]
    
    # Display sensor table
    sensor_df = pd.DataFrame(sensors)
    sensor_display_df = pd.DataFrame()
    sensor_display_df["Sensor ID"] = sensor_df["id"]
    sensor_display_df["Forest"] = sensor_df["forest"]
    sensor_display_df["Status"] = sensor_df["status"]
    sensor_display_df["Battery %"] = sensor_df["battery"]
    sensor_display_df["Detections"] = sensor_df["detections_today"]
    st.dataframe(
        sensor_display_df,
        width='stretch',
        hide_index=True
    )
    
    # Battery level chart
    st.subheader("🔋 Battery Levels")
    fig_battery = px.bar(
        sensor_df,
        x="id",
        y="battery",
        color="status",
        title="Sensor Battery Levels",
        labels={"id": "Sensor ID", "battery": "Battery Level (%)"}
    )
    st.plotly_chart(fig_battery, width='stretch')

# Deforestation analysis
st.subheader("📉 Deforestation Analysis")

# Filter deforestation data based on selected date range
df_deforest = pd.DataFrame(DEFORESTATION_DATA)
start_year = start_date.year
end_year = end_date.year
df_filtered = df_deforest[(df_deforest["year"] >= start_year) & (df_deforest["year"] <= end_year)]

# Deforestation trend chart
col1, col2 = st.columns(2)

with col1:
    fig_trend = px.line(
        df_filtered,
        x="year",
        y="area_hectares",
        color="location",
        title="Deforestation Trend Over Time",
        labels={"year": "Year", "area_hectares": "Area (Hectares)"}
    )
    st.plotly_chart(fig_trend, width='stretch')

with col2:
    # Deforestation by cause
    cause_data = df_filtered.groupby("cause")["area_hectares"].sum().reset_index()
    fig_cause = px.pie(
        cause_data,
        values="area_hectares",
        names="cause",
        title="Deforestation Causes"
    )
    st.plotly_chart(fig_cause, width='stretch')

# Detailed deforestation data table
st.subheader("📋 Detailed Deforestation Data")
df_display = pd.DataFrame()
df_display["Year"] = df_filtered["year"]
df_display["Location"] = df_filtered["location"]
df_display["Area Affected (ha)"] = df_filtered["area_hectares"]
df_display["Primary Cause"] = df_filtered["cause"]
st.dataframe(
    df_display,
    width='stretch'
)

# Conservation impact
st.subheader("🌱 Conservation Impact")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Trees Planted (2024)", 
        value="15,000",
        delta="↑ 25% from 2023"
    )

with col2:
    st.metric(
        label="Community Involvement", 
        value="2,450",
        delta="↑ 18% from 2023"
    )

with col3:
    st.metric(
        label="Protected Species", 
        value="34",
        delta="↑ 3 new species"
    )

# Footer
st.markdown("---")
st.markdown("🌳 Acoustic Guardian - Protecting Nairobi's forests with AI-powered acoustic monitoring")
st.markdown("Data updated daily | Last update: Today")