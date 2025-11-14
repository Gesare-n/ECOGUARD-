"""
Acoustic Guardian - Institutional Dashboard

Professional dashboard for Kenya Forest Service, NGOs, and research institutions
aligned with Wawa Gatheru's green economy vision.
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
    page_title="Acoustic Guardian - Institutional Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Kenya forest locations with realistic coordinates
FOREST_LOCATIONS = {
    "Karura Forest": {"lat": -1.2723, "lng": 36.8080, "area_km2": 17.5, "agency": "Nairobi City County"},
    "Ngong Forest": {"lat": -1.3500, "lng": 36.7000, "area_km2": 20.0, "agency": "KFS"},
    "Aberdare Forest": {"lat": -0.4500, "lng": 36.5000, "area_km2": 200.0, "agency": "KFS"},
    "Mt. Kenya Forest": {"lat": -0.2500, "lng": 37.7500, "area_km2": 150.0, "agency": "KFS"},
    "Arboretum Forest": {"lat": -0.5300, "lng": 36.5300, "area_km2": 5.0, "agency": "KEFRI"},
    "Kakamega Forest": {"lat": 0.3000, "lng": 34.7500, "area_km2": 70.0, "agency": "KFS"}
}

# Institutional partners
INSTITUTIONS = {
    "Kenya Forest Service (KFS)": {"type": "Government", "role": "Field Operations"},
    "Green Belt Movement": {"type": "NGO", "role": "Reforestation"},
    "KEFRI": {"type": "Research", "role": "Environmental Modeling"},
    "DeKUT": {"type": "Research", "role": "Innovation"},
    "WWF Kenya": {"type": "NGO", "role": "Conservation"},
    "Nairobi City County": {"type": "Government", "role": "Urban Forests"}
}

# Threat types
THREAT_TYPES = ["Chainsaw", "Vehicle", "Fire", "Encroachment", "Gunshot"]

# Mock sensor data generator
def generate_sensor_data():
    # Set seed for consistent data generation
    random.seed(42)
    sensors = []
    for i, (forest, coords) in enumerate(FOREST_LOCATIONS.items()):
        # Generate random detections for the past 24 hours
        detections = []
        for _ in range(random.randint(0, 10)):
            detection = {
                "timestamp": datetime.now() - timedelta(hours=random.randint(0, 24)),
                "threat_type": random.choice(THREAT_TYPES),
                "confidence": round(random.uniform(85, 99), 1),
                "lat": coords["lat"] + random.uniform(-0.005, 0.005),
                "lng": coords["lng"] + random.uniform(-0.005, 0.005)
            }
            detections.append(detection)
        
        sensor = {
            "id": f"AG-{str(i+1).zfill(3)}",
            "forest": forest,
            "agency": coords["agency"],
            "lat": coords["lat"],
            "lng": coords["lng"],
            "status": random.choice(["🟢 Active", "🟡 Warning", "🔴 Offline"]),
            "battery": round(random.uniform(70, 100), 1),
            "signal": random.randint(-80, -50),
            "detections_24h": len(detections),
            "last_detection": detections[-1] if detections else None,
            "detections": detections
        }
        sensors.append(sensor)
    return sensors

# Generate mock data
sensors = generate_sensor_data()

# Sidebar
st.sidebar.title("🌳 Acoustic Guardian")
st.sidebar.markdown("### Institutional Dashboard")

# Institution selector
selected_institution = st.sidebar.selectbox(
    "Select Institution",
    list(INSTITUTIONS.keys()),
    index=0
)

# Role-based access control
institution_info = INSTITUTIONS[selected_institution]
st.sidebar.markdown(f"**Type:** {institution_info['type']}")
st.sidebar.markdown(f"**Role:** {institution_info['role']}")

# Date range selector
st.sidebar.subheader("📅 Date Range")
date_range = st.sidebar.select_slider(
    "Select period",
    options=["24H", "7D", "30D", "90D", "1Y"],
    value="30D"
)

# Forest selector
st.sidebar.subheader("Forest Selection")
selected_forests = st.sidebar.multiselect(
    "Select Forests",
    list(FOREST_LOCATIONS.keys()),
    default=list(FOREST_LOCATIONS.keys())
)

# Threat type filter
st.sidebar.subheader("🚨 Threat Types")
selected_threats = st.sidebar.multiselect(
    "Filter by Threat Type",
    THREAT_TYPES,
    default=THREAT_TYPES
)

# Main dashboard
st.title("🌳 Acoustic Guardian - Institutional Forest Intelligence")
st.markdown(f"### Real-time monitoring for {selected_institution}")
st.markdown("---")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

# Filter sensors by selected forests
filtered_sensors = [s for s in sensors if s["forest"] in selected_forests]

# Calculate metrics
active_sensors = len([s for s in filtered_sensors if s["status"] == "🟢 Active"])
total_detections = sum([s["detections_24h"] for s in filtered_sensors])
avg_response_time = random.randint(2, 8)  # Mock response time in minutes
time_safe_avg = random.randint(120, 500)  # Mock time safe in hours

with col1:
    st.metric(
        label="Active Sensors", 
        value=active_sensors, 
        delta=f"{len(filtered_sensors)} total"
    )

with col2:
    st.metric(
        label="Detections (24H)", 
        value=total_detections,
        delta="↑ 12% from yesterday"
    )

with col3:
    st.metric(
        label="Avg Response Time", 
        value=f"{avg_response_time} min",
        delta="↓ 1 min from target"
    )

with col4:
    st.metric(
        label="Avg Time Safe", 
        value=f"{time_safe_avg} hrs",
        delta="↑ 15% improvement"
    )

# Map and recent alerts
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📍 Forest Monitoring Network")
    
    # Create map centered on Kenya
    m = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add forest markers
    for forest, coords in FOREST_LOCATIONS.items():
        if forest not in selected_forests:
            continue
            
        # Count recent detections for this forest
        forest_detections = sum([s["detections_24h"] for s in filtered_sensors if s["forest"] == forest])
        
        color = "red" if forest_detections > 0 else "green"
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Agency: {coords['agency']}<br>Area: {coords['area_km2']} km²<br>Recent Detections: {forest_detections}",
            tooltip=f"{forest} - {forest_detections} detections",
            icon=folium.Icon(color=color, icon="tree", prefix='fa')
        ).add_to(m)
        
        # Add sensor markers
        for sensor in filtered_sensors:
            if sensor["forest"] == forest:
                # Add sensor markers
                folium.CircleMarker(
                    location=[sensor["lat"], sensor["lng"]],
                    radius=8,
                    popup=f"Sensor {sensor['id']}<br>Status: {sensor['status']}<br>Detections (24H): {sensor['detections_24h']}",
                    color='blue' if sensor['status'] == '🟢 Active' else 'orange' if sensor['status'] == '🟡 Warning' else 'red',
                    fill=True,
                    fillColor='blue' if sensor['status'] == '🟢 Active' else 'orange' if sensor['status'] == '🟡 Warning' else 'red'
                ).add_to(m)
                
                # Add detection markers
                for detection in sensor["detections"]:
                    if detection["threat_type"] in selected_threats:
                        folium.CircleMarker(
                            location=[detection["lat"], detection["lng"]],
                            radius=6,
                            popup=f"Threat: {detection['threat_type']}<br>Confidence: {detection['confidence']}%<br>Time: {detection['timestamp'].strftime('%H:%M')}",
                            color='red',
                            fill=True,
                            fillColor='red'
                        ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("🚨 Recent Alerts")
    
    # Collect all recent detections
    all_detections = []
    for sensor in filtered_sensors:
        for detection in sensor["detections"]:
            if detection["threat_type"] in selected_threats:
                all_detections.append({
                    "timestamp": detection["timestamp"],
                    "sensor": sensor["id"],
                    "forest": sensor["forest"],
                    "threat": detection["threat_type"],
                    "confidence": detection["confidence"],
                    "agency": sensor["agency"]
                })
    
    # Sort by timestamp
    all_detections.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Display recent alerts
    if all_detections:
        df_alerts = pd.DataFrame(all_detections[:15])  # Show last 15 alerts
        alert_display_df = pd.DataFrame()
        alert_display_df["Time"] = df_alerts["timestamp"]
        alert_display_df["Forest"] = df_alerts["forest"]
        alert_display_df["Threat"] = df_alerts["threat"]
        alert_display_df["Confidence %"] = df_alerts["confidence"]
        st.dataframe(
            alert_display_df,
            width='stretch',
            hide_index=True
        )
    else:
        st.info("No recent alerts matching your filters")

# Threat analysis
st.subheader("🔍 Threat Analysis")

# Filter data for analysis
analysis_detections = []
for sensor in filtered_sensors:
    for detection in sensor["detections"]:
        if detection["threat_type"] in selected_threats:
            analysis_detections.append({
                "timestamp": detection["timestamp"],
                "threat_type": detection["threat_type"],
                "forest": sensor["forest"],
                "confidence": detection["confidence"],
                "agency": sensor["agency"]
            })

if analysis_detections:
    df_analysis = pd.DataFrame(analysis_detections)
    
    # Threat distribution
    col1, col2 = st.columns(2)
    
    with col1:
        threat_counts = df_analysis["threat_type"].value_counts().reset_index()
        threat_counts.columns = ["Threat Type", "Count"]
        fig_threats = px.pie(
            threat_counts,
            values="Count",
            names="Threat Type",
            title="Threat Distribution"
        )
        st.plotly_chart(fig_threats, width='stretch')
    
    with col2:
        forest_counts = df_analysis["forest"].value_counts().reset_index()
        forest_counts.columns = ["Forest", "Count"]
        fig_forests = px.bar(
            forest_counts,
            x="Forest",
            y="Count",
            color="Forest",
            title="Detections by Forest"
        )
        st.plotly_chart(fig_forests, width='stretch')
    
    # Timeline
    st.subheader("📈 Detection Timeline")
    df_timeline = df_analysis.copy()
    df_timeline["date"] = df_timeline["timestamp"].dt.date
    timeline_data = df_timeline.groupby(["date", "threat_type"]).size().reset_index()
    timeline_data.columns = ["date", "threat_type", "count"]
    
    fig_timeline = px.line(
        timeline_data,
        x="date",
        y="count",
        color="threat_type",
        title="Detections Over Time",
        markers=True
    )
    st.plotly_chart(fig_timeline, width='stretch')
else:
    st.info("No detection data available for analysis")

# Institutional metrics
st.subheader("📊 Institutional Performance")

# Show metrics relevant to the selected institution
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Areas Under Protection", 
        value=len([f for f in selected_forests if FOREST_LOCATIONS[f]["agency"] == selected_institution]),
        delta="↑ 2 new areas"
    )

with col2:
    st.metric(
        label="Response Rate", 
        value="94%",
        delta="↑ 3% from last quarter"
    )

with col3:
    st.metric(
        label="Data Quality Score", 
        value="8.7/10",
        delta="↑ 0.3 points"
    )

# Sustainability metrics
st.subheader("🌱 Sustainability Impact")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="CO2 Reduction", 
        value="1,240 tons",
        delta="↑ 15% this quarter"
    )

with col2:
    st.metric(
        label="Jobs Created", 
        value="42",
        delta="↑ 5 new positions"
    )

with col3:
    st.metric(
        label="Community Engagement", 
        value="1,850",
        delta="↑ 12% participation"
    )

with col4:
    st.metric(
        label="Research Partnerships", 
        value="8",
        delta="↑ 2 new collaborations"
    )

# Footer
st.markdown("---")
st.markdown("🌳 Acoustic Guardian - Empowering Kenya's forest protection ecosystem")
st.markdown(f"Data for {selected_institution} | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")