import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime
import folium
from streamlit_folium import st_folium
import sys
import os

# Add the scripts directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import auth

# Set page config
st.set_page_config(
    page_title="EcoGuard - Forest Protection",
    page_icon="🌳",
    layout="wide"
)

# Initialize session and check authentication
auth.init_session()

if not auth.is_logged_in():
    st.switch_page("login.py")

user = auth.get_current_user()

# Initialize session state
if 'detection_count' not in st.session_state:
    st.session_state.detection_count = 0
    
if 'time_safe' not in st.session_state:
    st.session_state.time_safe = 0
    
if 'last_detection' not in st.session_state:
    st.session_state.last_detection = None
    
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

# Function to simulate chainsaw detection
def simulate_detection():
    # Set seed for consistent data generation
    random.seed(42)
    # Simulate detection data
    detection_data = {
        'timestamp': datetime.now(),
        'device_id': 'AG-001',
        'location': 'Amazon-Brazil',
        'latitude': -3.4653,
        'longitude': -62.2159,
        'threat_type': 'Chainsaw',
        'confidence': round(random.uniform(90, 99), 1),
        'battery_level': round(random.uniform(85, 100), 1),
        'signal_strength': random.randint(-70, -50)
    }
    
    # Update session state
    st.session_state.detection_count += 1
    st.session_state.time_safe = 0
    st.session_state.last_detection = detection_data['timestamp']
    st.session_state.detection_history.append(detection_data)
    
    # Keep only last 10 detections
    if len(st.session_state.detection_history) > 10:
        st.session_state.detection_history = st.session_state.detection_history[-10:]
    
    return detection_data

# Function to simulate heartbeat
def simulate_heartbeat():
    # Set seed for consistent data generation
    random.seed(42)
    # Update time safe
    if st.session_state.last_detection:
        st.session_state.time_safe = int((datetime.now() - st.session_state.last_detection).total_seconds())
    
    # Simulate device status
    status_data = {
        'timestamp': datetime.now(),
        'battery_level': round(random.uniform(85, 100), 1),
        'signal_strength': random.randint(-70, -50),
        'uptime': random.randint(1000, 10000)
    }
    
    return status_data

# Sidebar
st.sidebar.title("EcoGuard")
st.sidebar.markdown(f"**User:** {user['name']}")
st.sidebar.markdown(f"**Role:** {auth.get_user_role_name(user['role'])}")
st.sidebar.markdown(f"**Region:** {user['region']}")

# Simulation controls
st.sidebar.subheader("Simulation Controls")
if st.sidebar.button("🚨 Simulate Chainsaw Detection"):
    detection_data = simulate_detection()
    st.sidebar.success(f"Detection simulated!\nConfidence: {detection_data['confidence']}%")

if st.sidebar.button("💚 Send Heartbeat"):
    status_data = simulate_heartbeat()
    st.sidebar.info("Heartbeat sent!")

# Reset button
if st.sidebar.button("🔄 Reset System"):
    st.session_state.detection_count = 0
    st.session_state.time_safe = 0
    st.session_state.last_detection = None
    st.session_state.detection_history = []
    st.sidebar.success("System reset!")

# Logout button
if st.sidebar.button("🚪 Logout"):
    auth.logout_user()
    st.switch_page("login.py")

# Main dashboard
st.title("🌳 EcoGuard - Forest Protection Dashboard")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active Sensors", 
        value="1", 
        delta="Online"
    )

with col2:
    st.metric(
        label="Detections Today", 
        value=st.session_state.detection_count,
        delta="↑ 1" if st.session_state.detection_count > 0 else None
    )

with col3:
    st.metric(
        label="Time Safe (minutes)", 
        value=f"{st.session_state.time_safe // 60}",
        delta="Reset" if st.session_state.time_safe == 0 and st.session_state.detection_count > 0 else None
    )

with col4:
    st.metric(
        label="System Status", 
        value="🟢 Active", 
        delta="Operational"
    )

# Map and detection history
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Sensor Location")
    
    # Create map
    m = folium.Map(
        location=[-3.4653, -62.2159],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add sensor marker
    folium.Marker(
        location=[-3.4653, -62.2159],
        popup=f"Sensor AG-001<br>Last Detection: {st.session_state.last_detection or 'None'}",
        tooltip="EcoGuard Sensor",
        icon=folium.Icon(color='green' if st.session_state.time_safe > 0 else 'red')
    ).add_to(m)
    
    # Add detection markers if any
    if st.session_state.detection_history:
        for detection in st.session_state.detection_history[-3:]:  # Show last 3 detections
            folium.CircleMarker(
                location=[detection['latitude'], detection['longitude']],
                radius=10,
                popup=f"Chainsaw Detected<br>Confidence: {detection['confidence']}%",
                color='red',
                fill=True,
                fillColor='red'
            ).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=400)

with col2:
    st.subheader("System Status")
    
    # Battery level
    random.seed(42)
    battery_level = random.uniform(85, 100)
    st.progress(battery_level/100)
    st.text(f"Battery: {battery_level:.1f}%")
    
    # Signal strength
    signal_strength = random.randint(-70, -50)
    signal_percent = max(0, min(100, (signal_strength + 100) * 2))  # Convert -100 to -50 dBm to 0-100%
    st.progress(signal_percent/100)
    st.text(f"Signal: {signal_strength} dBm")
    
    # Uptime
    uptime_hours = random.randint(24, 120)
    st.text(f"Uptime: {uptime_hours} hours")

# Detection history
st.subheader("Detection History")
if st.session_state.detection_history:
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.detection_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp', ascending=False)
    
    # Display table
    detection_display_df = pd.DataFrame()
    detection_display_df["Time"] = df["timestamp"]
    detection_display_df["Threat"] = df["threat_type"]
    detection_display_df["Confidence %"] = df["confidence"]
    detection_display_df["Latitude"] = df["latitude"]
    detection_display_df["Longitude"] = df["longitude"]
    st.dataframe(
        detection_display_df,
        width='stretch'
    )
else:
    st.info("No detections yet. Click 'Simulate Chainsaw Detection' to generate data.")

# Strategic layers information
st.subheader("Strategic Conservation Layers")
tab1, tab2, tab3 = st.tabs(["Deforestation Risk", "Protected Areas", "Reforestation Projects"])

with tab1:
    st.info("High-risk deforestation zones would be displayed here in the full implementation.")
    st.image("https://placehold.co/600x200?text=Deforestation+Risk+Map", caption="Deforestation Risk Zones")

with tab2:
    st.info("Protected forest areas would be displayed here in the full implementation.")
    st.image("https://placehold.co/600x200?text=Protected+Areas+Map", caption="Protected Forest Areas")

with tab3:
    st.info("Reforestation project locations would be displayed here in the full implementation.")
    st.image("https://placehold.co/600x200?text=Reforestation+Projects+Map", caption="Reforestation Projects")

# Footer
st.markdown("---")
st.markdown("🌳 EcoGuard - Protecting forests with AI-powered acoustic monitoring")