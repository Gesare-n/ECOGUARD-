import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime, timedelta
import random
import os

# Set page config
st.set_page_config(
    page_title="Acoustic Guardian - Super User Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

# Sidebar Navigation
st.sidebar.title("🌳 Acoustic Guardian")
st.sidebar.markdown("### Super User Control Center")

# Navigation menu
navigation_options = {
    "Overview": "🏠 Overview",
    "Main Dashboard": "🖥️ Main System",
    "Nairobi Dashboard": "绿城 Nairobi",
    "Institutional Dashboard": "🏢 Kenya Forest Service",
    "Policy Dashboard": "🏛️ Policy & Carbon Credit",
    "Research Dashboard": "🔬 Research",
    "Deforestation Analysis": "📉 Deforestation",
    "System Status": "📊 System Status"
}

# Create navigation buttons in sidebar
for page_key, page_label in navigation_options.items():
    if st.sidebar.button(page_label):
        st.session_state.current_page = page_key

# Main content based on navigation
current_page = st.session_state.current_page

if current_page == "Overview":
    # Main dashboard
    st.title("🌳 Acoustic Guardian - Super User Dashboard")
    st.markdown("### Centralized Access to All System Dashboards")
    
    # System Overview
    st.header("🌍 System Overview")
    
    # Key metrics across all systems
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Forests", 
            value="6", 
            delta="All monitored"
        )
    
    with col2:
        st.metric(
            label="Active Sensors", 
            value="18",
            delta="All online"
        )
    
    with col3:
        st.metric(
            label="Total Detections", 
            value="142",
            delta="↓ 3 from yesterday"
        )
    
    with col4:
        st.metric(
            label="Protected Area", 
            value="238.8 km²",
            delta="↑ 12 km² conserved"
        )
    
    # Forest locations map
    st.subheader("📍 All Forest Locations")
    
    # Forest locations data
    FOREST_LOCATIONS = {
        "Karura Forest": {"lat": -1.2723, "lng": 36.8080, "area_km2": 17.5},
        "Uhuru Park": {"lat": -1.3037, "lng": 36.8166, "area_km2": 0.6},
        "Central Park": {"lat": -1.2864, "lng": 36.8172, "area_km2": 0.5},
        "Jeevanjee Gardens": {"lat": -1.2833, "lng": 36.8222, "area_km2": 0.2},
        "Ngong Forest": {"lat": -1.3500, "lng": 36.7000, "area_km2": 20.0},
        "Aberdare Forest": {"lat": -0.4500, "lng": 36.5000, "area_km2": 200.0}
    }
    
    # Create map centered on Kenya
    m = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add forest markers
    for forest, coords in FOREST_LOCATIONS.items():
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²",
            tooltip=forest,
            icon=folium.Icon(color='green', icon="tree", prefix='fa')
        ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)
    
    # Dashboard Access Section
    st.header("🔗 Quick Access to All Dashboards")
    
    # Create cards for each dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏛️ Institutional Dashboards")
        
        if st.button("🏢 Kenya Forest Service Dashboard"):
            st.session_state.current_page = "Institutional Dashboard"
            
        if st.button("🏛️ Policy & Carbon Credit Dashboard"):
            st.session_state.current_page = "Policy Dashboard"
            
        if st.button("🔬 Research Dashboard"):
            st.session_state.current_page = "Research Dashboard"
        
        st.subheader("📊 Analysis Dashboards")
        
        if st.button("📉 Deforestation Analysis Dashboard"):
            st.session_state.current_page = "Deforestation Analysis"
    
    with col2:
        st.subheader("🌐 Regional Dashboards")
        
        if st.button("绿城 Nairobi Forest Dashboard"):
            st.session_state.current_page = "Nairobi Dashboard"
            
        st.subheader("⚙️ System Dashboards")
        
        if st.button("🖥️ Main System Dashboard"):
            st.session_state.current_page = "Main Dashboard"
    
    # System Status
    st.header("📊 System Status")
    
    # Mock system status data
    status_data = pd.DataFrame({
        'Dashboard': ['Institutional', 'Policy', 'Research', 'Nairobi', 'Deforestation', 'Main System'],
        'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active'],
        'Last Update': [datetime.now() - timedelta(minutes=random.randint(1, 10)) for _ in range(6)],
        'Response Time (ms)': [random.randint(50, 200) for _ in range(6)]
    })
    
    st.dataframe(status_data, width='stretch')
    
    # Footer
    st.markdown("---")
    st.markdown("🌳 Acoustic Guardian - Unified Forest Intelligence Platform")
    st.markdown("Super User Access | All Systems Operational")

elif current_page == "Main Dashboard":
    # Display content from the main dashboard
    st.title("🖥️ Main System Dashboard")
    st.markdown("### Core Acoustic Guardian Monitoring System")
    
    # Add a simple iframe to show the main dashboard (in a real implementation, this would be the actual dashboard content)
    st.info("In a full implementation, this would display the main dashboard content directly.")
    st.markdown("""
    The main dashboard includes:
    - Real-time forest protection monitoring
    - Chainsaw detection simulation
    - Interactive map showing sensor locations
    - Detection history tracking
    - System status monitoring
    """)
    
    # Show a placeholder map
    m = folium.Map(
        location=[-3.4653, -62.2159],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    folium.Marker(
        location=[-3.4653, -62.2159],
        popup="Sensor AG-001",
        tooltip="Acoustic Guardian Sensor",
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    st_folium(m, width=700, height=400)
    
    st.markdown("---")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8501")

elif current_page == "Nairobi Dashboard":
    # Display content from the Nairobi dashboard
    st.title("绿城 Nairobi Forest Conservation Dashboard")
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
    
    # Show a Nairobi map
    m = folium.Map(
        location=[-1.2921, 36.8219],  # Center of Nairobi
        zoom_start=11,
        tiles='OpenStreetMap'
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
    
    # Add forest markers
    for forest, coords in FOREST_LOCATIONS.items():
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²",
            tooltip=forest,
            icon=folium.Icon(color='green', icon="tree", prefix='fa')
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    st.markdown("---")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8505")

elif current_page == "Institutional Dashboard":
    st.title("🏢 Kenya Forest Service Dashboard")
    st.markdown("### Institutional Forest Management Interface")
    
    st.info("In a full implementation, this would display the institutional dashboard content directly.")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8502")

elif current_page == "Policy Dashboard":
    st.title("🏛️ Policy & Carbon Credit Dashboard")
    st.markdown("### Policy Analysis and Carbon Credit Tracking")
    
    st.info("In a full implementation, this would display the policy dashboard content directly.")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8503")

elif current_page == "Research Dashboard":
    st.title("🔬 Research Dashboard")
    st.markdown("### Scientific Research and Data Analysis")
    
    st.info("In a full implementation, this would display the research dashboard content directly.")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8504")

elif current_page == "Deforestation Analysis":
    st.title("📉 Deforestation Analysis Dashboard")
    st.markdown("### Deforestation Trends and Analysis")
    
    st.info("In a full implementation, this would display the deforestation analysis dashboard content directly.")
    st.markdown("To access the live dashboard, navigate to: http://localhost:8506")

elif current_page == "System Status":
    st.title("📊 System Status Dashboard")
    st.markdown("### Real-time System Health and Performance")
    
    # Mock system status data
    status_data = pd.DataFrame({
        'Dashboard': ['Institutional', 'Policy', 'Research', 'Nairobi', 'Deforestation', 'Main System'],
        'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active'],
        'Last Update': [datetime.now() - timedelta(minutes=random.randint(1, 10)) for _ in range(6)],
        'Response Time (ms)': [random.randint(50, 200) for _ in range(6)]
    })
    
    st.dataframe(status_data, width='stretch')
    
    # Add some performance charts
    st.subheader("📈 System Performance")
    performance_data = pd.DataFrame({
        'Time': pd.date_range(start='1/1/2024', periods=10, freq='H'),
        'CPU %': [random.randint(20, 80) for _ in range(10)],
        'Memory %': [random.randint(30, 70) for _ in range(10)],
        'Network MB/s': [random.randint(5, 50) for _ in range(10)]
    })
    
    st.line_chart(performance_data.set_index('Time'))