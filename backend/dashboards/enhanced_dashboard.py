"""
Enhanced EcoGuard Dashboard with Role-Based Access Control
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import sys
import os

# Add the scripts directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import auth

# Set page config
st.set_page_config(
    page_title="EcoGuard - Enhanced Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Initialize session and check authentication
auth.init_session()

if not auth.is_logged_in():
    st.switch_page("login.py")

user = auth.get_current_user()
user_role = user['role']

# Load Kenya forest data
@st.cache_data
def load_forest_data():
    """Load Kenya forest data"""
    forest_data = {
        "name": ["Karura Forest", "Uhuru Park", "Ngong Forest", "Aberdare Forest", "Mt. Kenya Forest", "Arboretum Forest", "Kakamega Forest", "Mau Forest", "Chyulu Hills Forest", "Taita Hills Forest"],
        "lat": [-1.2723, -1.3037, -1.3500, -0.4500, -0.2500, -0.5300, 0.3000, -0.5000, -2.5000, -3.5000],
        "lng": [36.8080, 36.8166, 36.7000, 36.5000, 37.7500, 36.5300, 34.7500, 35.5000, 38.0000, 38.5000],
        "area_km2": [17.5, 0.6, 20.0, 200.0, 150.0, 5.0, 70.0, 400.0, 150.0, 25.0],
        "type": ["Urban Forest", "Urban Park", "Indigenous Forest", "Mountain Forest", "Mountain Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest", "Indigenous Forest"],
        "region": ["Nairobi", "Nairobi", "Nairobi", "Central", "Central", "Central", "Western", "Rift Valley", "Coastal", "Coastal"]
    }
    return pd.DataFrame(forest_data)

# Load deforestation risk model
@st.cache_data
def load_risk_data():
    """Load deforestation risk model data"""
    risk_data = {
        "forest": ["Karura Forest", "Uhuru Park", "Ngong Forest", "Aberdare Forest", "Mt. Kenya Forest", "Kakamega Forest"],
        "urban_proximity": [0.9, 1.0, 0.7, 0.2, 0.3, 0.4],
        "accessibility": [0.8, 1.0, 0.7, 0.4, 0.5, 0.6],
        "historical_loss": [0.3, 0.8, 0.5, 0.2, 0.1, 0.6],
        "risk_score": [0.67, 0.93, 0.63, 0.27, 0.30, 0.53]
    }
    return pd.DataFrame(risk_data)

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
        "type": row['type'],
        "region": row['region']
    }

# Filter data based on user role and region
def filter_data_by_role_and_region(df):
    """Filter data based on user role and region"""
    if user_role == 'super_user':
        return df  # Super users see all data
    elif user_role == 'regional_manager':
        # Regional managers see data for their region
        region = user['region']
        if region != "All Regions":
            return df[df['region'] == region]
        return df
    else:
        # Forest rangers see data for their region
        region = user['region']
        return df[df['region'] == region]

# Sidebar
st.sidebar.title("EcoGuard")
st.sidebar.markdown(f"**User:** {user['name']}")
st.sidebar.markdown(f"**Role:** {auth.get_user_role_name(user_role)}")
st.sidebar.markdown(f"**Region:** {user['region']}")

# Navigation
st.sidebar.subheader("Navigation")
page_options = ["Overview", "Forest Map", "Deforestation Analysis", "Sensor Status", "Reports"]

# Add user management for super users
if user_role == 'super_user':
    page_options.append("User Management")

page = st.sidebar.selectbox(
    "Select Page",
    page_options
)

# Profile link
if st.sidebar.button("👤 My Profile"):
    st.switch_page("profile.py")

# Logout button
if st.sidebar.button("🚪 Logout"):
    auth.logout_user()
    st.switch_page("login.py")

# Main content based on navigation
if page == "Overview":
    st.title("🌳 EcoGuard - Forest Protection Dashboard")
    
    # Filter data for user's region
    filtered_forest_data = filter_data_by_role_and_region(forest_data)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Forests in Region", 
            value=len(filtered_forest_data), 
            delta="All monitored"
        )
    
    with col2:
        st.metric(
            label="Active Sensors", 
            value=max(1, len(filtered_forest_data) * 2),  # Simplified calculation
            delta="All online"
        )
    
    with col3:
        st.metric(
            label="Detections (Today)", 
            value=np.random.randint(0, 10),  # Mock data
            delta="↑ 2 from yesterday" if np.random.rand() > 0.5 else "↓ 1 from yesterday"
        )
    
    with col4:
        total_area = filtered_forest_data['area_km2'].sum()
        st.metric(
            label="Protected Area", 
            value=f"{total_area:.1f} km²",
            delta="↑ Conserving" if total_area > 0 else None
        )
    
    # Forest map
    st.subheader("📍 Forest Locations")
    
    # Create map centered on user's region
    if user_role == 'super_user':
        center_coords = [-0.0236, 37.9062]  # Center of Kenya
        zoom_level = 7
    elif user['region'] == 'Nairobi':
        center_coords = [-1.2921, 36.8219]  # Center of Nairobi
        zoom_level = 11
    elif user['region'] == 'Central':
        center_coords = [-0.4500, 36.5000]  # Aberdare Forest area
        zoom_level = 9
    else:
        # Default to Kenya center
        center_coords = [-0.0236, 37.9062]
        zoom_level = 7
    
    m = folium.Map(
        location=center_coords,
        zoom_start=zoom_level,
        tiles='OpenStreetMap'
    )
    
    # Add forest markers with different colors based on type
    for forest, coords in FOREST_LOCATIONS.items():
        # Only show forests in user's region (unless super user)
        if user_role != 'super_user' and coords['region'] != user['region']:
            continue
            
        color = "green"
        if coords["type"] == "Urban Forest":
            color = "darkgreen"
        elif coords["type"] == "Urban Park":
            color = "lightgreen"
        elif coords["type"] == "Mountain Forest":
            color = "darkblue"
        elif coords["type"] == "Indigenous Forest":
            color = "forestgreen"
        
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²<br>Type: {coords['type']}",
            tooltip=forest,
            icon=folium.Icon(color=color, icon="tree", prefix='fa')
        ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    # Mock recent activity data
    activity_data = [
        {"time": "2 hours ago", "event": "Chainsaw detected", "location": "Karura Forest", "confidence": "94%"},
        {"time": "5 hours ago", "event": "Sensor heartbeat", "location": "Ngong Forest", "confidence": "Normal"},
        {"time": "1 day ago", "event": "New sensor deployed", "location": "Uhuru Park", "confidence": "Successful"},
    ]
    
    for activity in activity_data:
        st.markdown(f"- **{activity['time']}**: {activity['event']} at {activity['location']} ({activity['confidence']})")

elif page == "Forest Map":
    st.title("🗺️ Forest Map")
    
    # Create map with all forests
    m = folium.Map(
        location=[-0.0236, 37.9062],  # Center of Kenya
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add forest markers with different colors based on type
    for forest, coords in FOREST_LOCATIONS.items():
        # Only show forests in user's region (unless super user)
        if user_role != 'super_user' and coords['region'] != user['region']:
            continue
            
        color = "green"
        if coords["type"] == "Urban Forest":
            color = "darkgreen"
        elif coords["type"] == "Urban Park":
            color = "lightgreen"
        elif coords["type"] == "Mountain Forest":
            color = "darkblue"
        elif coords["type"] == "Indigenous Forest":
            color = "forestgreen"
        
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²<br>Type: {coords['type']}",
            tooltip=forest,
            icon=folium.Icon(color=color, icon="tree", prefix='fa')
        ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=600)

elif page == "Deforestation Analysis":
    st.title("📉 Deforestation Analysis")
    
    # Filter risk data for user's region
    if user_role != 'super_user':
        risk_data_filtered = risk_data[
            risk_data['forest'].isin([
                f for f, coords in FOREST_LOCATIONS.items() 
                if coords['region'] == user['region']
            ])
        ]
    else:
        risk_data_filtered = risk_data
    
    if not risk_data_filtered.empty:
        # Risk scores chart
        fig_risk = px.bar(
            risk_data_filtered,
            x="forest",
            y="risk_score",
            title="Deforestation Risk Scores by Forest",
            labels={"risk_score": "Risk Score (0-1)", "forest": "Forest"}
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Detailed risk factors
        st.subheader("🔍 Risk Factor Analysis")
        st.dataframe(risk_data_filtered, use_container_width=True)
    else:
        st.info("No deforestation risk data available for your region.")

elif page == "Sensor Status":
    st.title("📡 Sensor Status")
    
    # Mock sensor data
    sensor_data = []
    for i, (forest, coords) in enumerate(list(FOREST_LOCATIONS.items())[:6]):
        # Only show sensors in user's region (unless super user)
        if user_role != 'super_user' and coords['region'] != user['region']:
            continue
            
        sensor = {
            "id": f"AG-{str(i+1).zfill(3)}",
            "forest": forest,
            "status": np.random.choice(["🟢 Active", "🟡 Warning", "🔴 Offline"]),
            "battery": round(np.random.uniform(70, 100), 1),
            "signal": np.random.randint(-80, -50),
            "last_seen": f"{np.random.randint(1, 24)} hours ago"
        }
        sensor_data.append(sensor)
    
    if sensor_data:
        sensor_df = pd.DataFrame(sensor_data)
        st.dataframe(sensor_df, use_container_width=True)
        
        # Battery level chart
        fig_battery = px.bar(
            sensor_df,
            x="id",
            y="battery",
            color="status",
            title="Sensor Battery Levels",
            labels={"id": "Sensor ID", "battery": "Battery Level (%)"}
        )
        st.plotly_chart(fig_battery, use_container_width=True)
    else:
        st.info("No sensors deployed in your region.")

elif page == "Reports":
    st.title("📋 Reports")
    
    # Only super users and regional managers can access detailed reports
    if user_role in ['super_user', 'regional_manager']:
        report_type = st.selectbox(
            "Select Report Type",
            ["Monthly Summary", "Quarterly Analysis", "Annual Report"]
        )
        
        if report_type == "Monthly Summary":
            st.subheader("📊 Monthly Summary Report")
            
            # Mock monthly data
            monthly_data = {
                "Metric": ["Detections", "False Positives", "Sensor Uptime", "New Deployments", "Maintenance Events"],
                "Value": [42, 3, "98.7%", 2, 5],
                "Trend": ["↑ 12%", "↓ 5%", "↑ 0.3%", "↑ 2 units", "↓ 1 event"]
            }
            monthly_df = pd.DataFrame(monthly_data)
            st.dataframe(monthly_df, use_container_width=True)
            
        elif report_type == "Quarterly Analysis":
            st.subheader("📈 Quarterly Analysis Report")
            st.info("Detailed quarterly analysis would be displayed here.")
            
        elif report_type == "Annual Report":
            st.subheader("📅 Annual Report")
            st.info("Comprehensive annual report would be displayed here.")
    else:
        st.warning("Access to detailed reports is restricted to Regional Managers and Super Users.")
        st.info("As a Forest Ranger, you can view your daily activity summary in the Overview section.")

elif page == "User Management":
    # Show user management page for super users
    st.info("Redirecting to user management...")
    st.switch_page("user_management.py")

# Footer
st.markdown("---")
st.markdown(f"🌳 EcoGuard - Protecting forests with AI-powered acoustic monitoring | User: {user['name']} ({auth.get_user_role_name(user_role)})")