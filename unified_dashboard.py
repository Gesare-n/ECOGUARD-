import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os

# Import Google Maps API key
try:
    from dashboard_config import GOOGLE_MAPS_API_KEY
except ImportError:
    GOOGLE_MAPS_API_KEY = None

# Set page config
st.set_page_config(
    page_title="EcoGuard - Unified Forest Intelligence Platform",
    page_icon="🌳",
    layout="wide"
)

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

# Mock carbon credit data
def generate_carbon_data(forest_locations):
    """Generate mock carbon credit data"""
    # Set seed for consistent data generation
    random.seed(42)
    data = []
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(365):
        date = base_date + timedelta(days=i)
        
        # Simulate decreasing deforestation over time (improvement)
        reduction_factor = 1 - (i / 365) * 0.6  # 60% improvement over the year
        
        for forest, info in forest_locations.items():
            # Base deforestation (hectares)
            base_deforestation = random.uniform(0.1, 2.0)
            actual_deforestation = base_deforestation * reduction_factor
            
            # Calculate carbon impact
            carbon_per_hectare = info.get("carbon_tons_per_km2", 150000) / 100  # Convert to per hectare
            carbon_loss = actual_deforestation * carbon_per_hectare
            
            # Calculate protection effectiveness
            protection_mapping = {
                "Highly Protected": 0.95,
                "Well Protected": 0.85,
                "Moderated Protected": 0.70,
                "Moderately Protected": 0.70
            }
            protection_effectiveness = protection_mapping.get(info.get("protection_status", "Moderated Protected"), 0.70)
            
            record = {
                "date": date,
                "forest": forest,
                "deforestation_ha": round(actual_deforestation, 2),
                "carbon_loss_tons": round(carbon_loss, 2),
                "protection_status": info.get("protection_status", "Moderated Protected"),
                "protection_effectiveness": protection_effectiveness,
                "total_carbon_stored": round(info["area_km2"] * info.get("carbon_tons_per_km2", 150000) * (1 - i/365 * 0.1), 0)
            }
            data.append(record)
    
    return pd.DataFrame(data)

# Mock sensor data
def generate_sensor_data(forest_locations):
    """Generate mock sensor data"""
    # Set seed for consistent data generation
    random.seed(42)
    sensors = []
    for i, (forest, coords) in enumerate(forest_locations.items()):
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

# Mock deforestation data
def generate_deforestation_data():
    """Generate mock deforestation data"""
    return [
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
        "carbon_tons_per_km2": 150000,  # Default value
        "protection_status": "Moderated Protected"  # Default value
    }

# Add carbon data to forest locations
for _, row in risk_data.iterrows():
    if row['forest'] in FOREST_LOCATIONS:
        FOREST_LOCATIONS[row['forest']]['risk_score'] = row['risk_score']

# Generate mock data
sensor_data = generate_sensor_data(FOREST_LOCATIONS)
carbon_data = generate_carbon_data(FOREST_LOCATIONS)
deforestation_data = generate_deforestation_data()

# Sidebar Navigation
st.sidebar.title("🌳 EcoGuard")
st.sidebar.markdown("### Unified Forest Intelligence Platform")

# Navigation menu
navigation_options = {
    "Overview": "🏠 System Overview",
    "Forest Monitoring": "🌲 Forest Monitoring",
    "Reforestation": "🌱 Reforestation Tracking",
    "Deforestation": "🔥 Deforestation Analysis",
    "Carbon Credits": "🪙 Carbon Credit Analytics",
    "Sensor Network": "📡 Sensor Management",
    "Nursery Monitoring": "🌿 Nursery Management",
    "Policy Insights": "📜 Policy Development"
}

# Create navigation buttons in sidebar
selected_page = st.sidebar.selectbox("Navigate to:", list(navigation_options.values()))
current_page = [k for k, v in navigation_options.items() if v == selected_page][0]

# Main content based on navigation
if current_page == "Overview":
    st.title("🌳 EcoGuard - Unified Forest Intelligence Platform")
    st.markdown("### Centralized Forest Conservation and Monitoring System")
    
    # System Overview
    st.header("🌍 System Overview")
    
    # Key metrics across all systems
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Forests", 
            value=len(FOREST_LOCATIONS), 
            delta="All monitored"
        )
    
    with col2:
        active_sensors = len([s for s in sensor_data if "Active" in s["status"]])
        st.metric(
            label="Active Sensors", 
            value=active_sensors,
            delta="All online"
        )
    
    with col3:
        total_detections = sum([s["detections_today"] for s in sensor_data])
        st.metric(
            label="Total Detections", 
            value=total_detections,
            delta="↓ 3 from yesterday"
        )
    
    with col4:
        total_area = sum([coords["area_km2"] for coords in FOREST_LOCATIONS.values()])
        st.metric(
            label="Protected Area", 
            value=f"{total_area:.1f} km²",
            delta="↑ 12 km² conserved"
        )
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Forest Locations", "📊 System Status", "📈 Carbon Impact", "🛡️ Risk Assessment"])
    
    with tab1:
        st.subheader("📍 All Forest Locations in Kenya")
        
        # Create map centered on Kenya with Google Maps
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
        
        # Add forest markers with different colors based on type
        for forest, coords in FOREST_LOCATIONS.items():
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
            ).add_to(m1)
        
        # Display map
        st_folium(m1, width=700, height=500)
        
        # Forest statistics
        st.subheader("📊 Forest Statistics")
        forest_types = forest_data['type'].value_counts()
        fig_forest_types = px.pie(
            values=forest_types.values,
            names=forest_types.index,
            title="Distribution of Forest Types"
        )
        st.plotly_chart(fig_forest_types, width='stretch')
    
    with tab2:
        st.subheader("📊 System Status")
        
        # Mock system status data
        status_data = pd.DataFrame({
            'Dashboard': ['Main System', 'Institutional', 'Policy', 'Research', 'Nairobi', 'Deforestation'],
            'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active'],
            'Last Update': [datetime.now() - timedelta(minutes=random.randint(1, 10)) for _ in range(6)],
            'Response Time (ms)': [random.randint(50, 200) for _ in range(6)]
        })
        
        st.dataframe(status_data, width='stretch')
    
    with tab3:
        st.subheader("📈 Carbon Impact")
        
        # Carbon data summary
        total_deforestation = sum([d["area_hectares"] for d in deforestation_data])
        st.metric(
            label="Total Deforestation Prevented", 
            value=f"{total_deforestation:,.0f} ha",
            delta="Since system deployment"
        )
        
        # Carbon storage trend
        carbon_storage = carbon_data.groupby("date")["total_carbon_stored"].mean().reset_index()
        fig_storage = px.line(
            carbon_storage,
            x="date",
            y="total_carbon_stored",
            title="Forest Carbon Storage Over Time",
            labels={"date": "Date", "total_carbon_stored": "Carbon Stored (tons)"}
        )
        st.plotly_chart(fig_storage, width='stretch')
    
    with tab4:
        st.subheader("🛡️ Risk Assessment")
        
        # Risk assessment table
        if not risk_data.empty:
            st.dataframe(risk_data, width='stretch')
        else:
            st.info("No risk assessment data available.")

elif current_page == "Forest Monitoring":
    st.title("🌲 Forest Monitoring Dashboard")
    st.markdown("### Real-time monitoring of all forest locations")
    
    # Forest monitoring content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📍 Forest Locations & Sensor Network")
        
        # Create map centered on Kenya with Google Maps
        m = folium.Map(
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
        
        # Add forest markers
        for forest, coords in FOREST_LOCATIONS.items():
            color = "green"
            folium.Marker(
                location=[coords["lat"], coords["lng"]],
                popup=f"<b>{forest}</b><br>Area: {coords['area_km2']} km²<br>Type: {coords['type']}",
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
        
        # Sensor status table
        sensor_df = pd.DataFrame(sensor_data)
        st.dataframe(sensor_df[["id", "forest", "status", "battery", "detections_today"]], width='stretch')
        
        # Sensor status distribution
        status_counts = sensor_df['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Sensor Status Distribution"
        )
        st.plotly_chart(fig_status, width='stretch')

elif current_page == "Reforestation":
    st.title("🌱 Reforestation Tracking")
    st.markdown("### Monitoring newly planted areas and growth progress")
    
    # Mock reforestation data
    reforestation_data = [
        {"area": "Karura Forest - Northern Section", "lat": -1.2650, "lng": 36.8100, "hectares": 15, "trees_planted": 2500, "planting_date": "2024-01-15"},
        {"area": "Ngong Forest - Eastern Edge", "lat": -1.3450, "lng": 36.7100, "hectares": 8, "trees_planted": 1200, "planting_date": "2024-02-20"},
        {"area": "Arboretum Forest - Southern Zone", "lat": -0.5400, "lng": 36.5200, "hectares": 3, "trees_planted": 800, "planting_date": "2024-03-10"},
        {"area": "Mau Forest - Restoration Zone A", "lat": -0.4800, "lng": 35.4800, "hectares": 45, "trees_planted": 6500, "planting_date": "2024-01-30"}
    ]
    
    # Create map for reforestation areas with Google Maps
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
    
    # Display map
    st_folium(m2, width=700, height=500)
    
    # Reforestation statistics
    st.subheader("📊 Reforestation Progress")
    reforestation_df = pd.DataFrame(reforestation_data)
    st.dataframe(reforestation_df, width='stretch')
    
    total_hectares = sum([area["hectares"] for area in reforestation_data])
    total_trees = sum([area["trees_planted"] for area in reforestation_data])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Reforested Area", f"{total_hectares} hectares")
    with col2:
        st.metric("Total Trees Planted", f"{total_trees:,}")

elif current_page == "Deforestation":
    st.title("🔥 Deforestation Analysis")
    st.markdown("### Tracking and analyzing deforestation patterns")
    
    # Mock deforestation data
    deforestation_data = [
        {"area": "Mau Forest - Western Section", "lat": -0.5200, "lng": 35.4500, "hectares_lost": 120, "year": 2023, "cause": "Agricultural Expansion"},
        {"area": "Kakamega Forest - Northern Edge", "lat": 0.3200, "lng": 34.7300, "hectares_lost": 45, "year": 2023, "cause": "Illegal Logging"},
        {"area": "Taita Hills Forest", "lat": -3.4800, "lng": 38.4800, "hectares_lost": 18, "year": 2023, "cause": "Charcoal Production"},
        {"area": "Chyulu Hills Forest - Southern Zone", "lat": -2.5200, "lng": 37.9800, "hectares_lost": 32, "year": 2023, "cause": "Settlements"}
    ]
    
    # Create map for deforestation areas with Google Maps
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
    
    # Display map
    st_folium(m3, width=700, height=500)
    
    # Deforestation statistics
    st.subheader("📉 Deforestation Analysis")
    deforestation_df = pd.DataFrame(deforestation_data)
    st.dataframe(deforestation_df, width='stretch')
    
    total_lost = sum([area["hectares_lost"] for area in deforestation_data])
    st.metric("Total Forest Area Lost (2023)", f"{total_lost} hectares")
    
    # Deforestation by cause
    cause_data = deforestation_df.groupby("cause")["hectares_lost"].sum().reset_index()
    fig_cause = px.pie(
        cause_data,
        values="hectares_lost",
        names="cause",
        title="Deforestation Causes"
    )
    st.plotly_chart(fig_cause, width='stretch')

elif current_page == "Carbon Credits":
    st.title("🪙 Carbon Credit Analytics")
    st.markdown("### Tracking carbon storage and credit potential")
    
    # Carbon credit content
    # Key carbon metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_deforestation = carbon_data["deforestation_ha"].sum()
    total_carbon_loss = carbon_data["carbon_loss_tons"].sum()
    avg_protection = carbon_data["protection_effectiveness"].mean()
    
    with col1:
        st.metric(
            label="Total Deforestation", 
            value=f"{total_deforestation:,.1f} ha",
            delta=f"{-total_deforestation:,.1f} ha prevented"
        )
    
    with col2:
        st.metric(
            label="Carbon Loss Prevented", 
            value=f"{total_carbon_loss:,.0f} tons",
            delta="CO2 equivalent"
        )
    
    with col3:
        st.metric(
            label="Protection Effectiveness", 
            value=f"{avg_protection:.1%}",
            delta="Above target" if avg_protection > 0.8 else "Needs improvement"
        )
    
    with col4:
        # Calculate carbon credits (assuming $5 per ton)
        carbon_credits_value = total_carbon_loss * 5
        st.metric(
            label="Carbon Credit Value", 
            value=f"${carbon_credits_value:,.0f}",
            delta="Potential revenue"
        )
    
    # Carbon storage over time
    st.subheader("📈 Carbon Storage Trends")
    carbon_storage = carbon_data.groupby("date")["total_carbon_stored"].mean().reset_index()
    
    fig_storage = px.line(
        carbon_storage,
        x="date",
        y="total_carbon_stored",
        title="Forest Carbon Storage Over Time",
        labels={"date": "Date", "total_carbon_stored": "Carbon Stored (tons)"}
    )
    st.plotly_chart(fig_storage, width='stretch')
    
    # Deforestation by forest
    st.subheader("🌲 Deforestation by Forest")
    deforestation_by_forest = carbon_data.groupby("forest")["deforestation_ha"].sum().reset_index()
    deforestation_by_forest = deforestation_by_forest.sort_values("deforestation_ha", ascending=False)
    
    fig_deforestation = px.bar(
        deforestation_by_forest,
        x="forest",
        y="deforestation_ha",
        color="deforestation_ha",
        color_continuous_scale="Reds",
        title="Total Deforestation by Forest (Hectares)",
        labels={"forest": "Forest", "deforestation_ha": "Deforestation (ha)"}
    )
    st.plotly_chart(fig_deforestation, width='stretch')

elif current_page == "Sensor Network":
    st.title("📡 Sensor Network Management")
    st.markdown("### Managing and monitoring all sensor devices")
    
    # Sensor network content
    # Sensor status table
    sensor_df = pd.DataFrame(sensor_data)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sensors", 
            value=len(sensor_data), 
            delta="All deployed"
        )
    
    with col2:
        active_sensors = len([s for s in sensor_data if "Active" in s["status"]])
        st.metric(
            label="Active Sensors", 
            value=active_sensors,
            delta=f"{active_sensors/len(sensor_data):.0%} operational"
        )
    
    with col3:
        avg_battery = sum([s["battery"] for s in sensor_data]) / len(sensor_data)
        st.metric(
            label="Avg Battery Level", 
            value=f"{avg_battery:.1f}%",
            delta="Good condition"
        )
    
    with col4:
        total_detections = sum([s["detections_today"] for s in sensor_data])
        st.metric(
            label="Today's Detections", 
            value=total_detections,
            delta="Real-time monitoring"
        )
    
    # Sensor status table
    st.subheader("📊 Sensor Status Overview")
    st.dataframe(sensor_df, width='stretch')
    
    # Sensor status distribution
    st.subheader("📶 Sensor Status Distribution")
    status_counts = sensor_df['status'].value_counts()
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Sensor Status Distribution"
    )
    st.plotly_chart(fig_status, width='stretch')
    
    # Battery level distribution
    st.subheader("🔋 Battery Level Distribution")
    fig_battery = px.histogram(
        sensor_df,
        x="battery",
        nbins=20,
        title="Sensor Battery Levels",
        labels={"battery": "Battery Level (%)"}
    )
    st.plotly_chart(fig_battery, width='stretch')

elif current_page == "Nursery Monitoring":
    st.title("🌿 Nursery Management")
    st.markdown("### Monitoring tree nurseries and seedling health")
    
    # Mock nursery and reforestation monitoring data
    nursery_data = [
        {"name": "Karura Forest Nursery", "lat": -1.2700, "lng": 36.8100, "seedlings": 5000, "species": "Indigenous Trees", "status": "Healthy", "last_review": "2024-05-15", "next_review": "2024-06-15"},
        {"name": "Ngong Forest Seed Bank", "lat": -1.3400, "lng": 36.6900, "seedlings": 12000, "species": "Acacia, Croton", "status": "Needs Attention", "last_review": "2024-04-22", "next_review": "2024-05-22"},
        {"name": "Aberdare Reforestation Hub", "lat": -0.4400, "lng": 36.4900, "seedlings": 8500, "species": "Oak, Cedar", "status": "Healthy", "last_review": "2024-05-10", "next_review": "2024-06-10"},
        {"name": "Kakamega Tree Farm", "lat": 0.2900, "lng": 34.7400, "seedlings": 6200, "species": "Indigenous Shade Trees", "status": "Excellent", "last_review": "2024-05-18", "next_review": "2024-06-18"},
        {"name": "Mau Forest Greenhouse", "lat": -0.4900, "lng": 35.4900, "seedlings": 15000, "species": "Various Native Species", "status": "Critical", "last_review": "2024-03-30", "next_review": "2024-05-30"}
    ]
    
    # Create map for nursery locations with Google Maps
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
    
    # Display map
    st_folium(m5, width=700, height=500)
    
    # Nursery statistics
    st.subheader("📊 Nursery Statistics")
    nursery_df = pd.DataFrame(nursery_data)
    st.dataframe(nursery_df, width='stretch')
    
    # Status distribution chart
    status_counts = nursery_df['status'].value_counts()
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Nursery Health Status Distribution"
    )
    st.plotly_chart(fig_status, width='stretch')
    
    # Reviews due soon
    st.subheader("⏰ Upcoming Reviews")
    today = datetime.today().date()
    upcoming_reviews = []
    for nursery in nursery_data:
        next_review_date = datetime.strptime(nursery["next_review"], "%Y-%m-%d").date()
        days_until = (next_review_date - today).days
        if days_until <= 30:  # Within 30 days
            upcoming_reviews.append({
                "Nursery": nursery["name"],
                "Review Date": nursery["next_review"],
                "Days Until": days_until,
                "Status": nursery["status"]
            })
    
    if upcoming_reviews:
        upcoming_df = pd.DataFrame(upcoming_reviews)
        st.dataframe(upcoming_df.sort_values("Days Until"), width='stretch')
    else:
        st.info("No reviews scheduled within the next 30 days.")

elif current_page == "Policy Insights":
    st.title("📜 Policy Development Insights")
    st.markdown("### Data-driven insights for forest policy and carbon credits")
    
    # Policy insights content
    # Policy impact metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate policy metrics
    total_forest_area = sum([FOREST_LOCATIONS[f]["area_km2"] for f in FOREST_LOCATIONS])
    protected_area = sum([FOREST_LOCATIONS[f]["area_km2"] for f in FOREST_LOCATIONS 
                         if FOREST_LOCATIONS[f].get("protection_status", "Moderated Protected") in ["Highly Protected", "Well Protected"]])
    protection_rate = protected_area / total_forest_area if total_forest_area > 0 else 0
    
    with col1:
        st.metric(
            label="Total Forest Area", 
            value=f"{total_forest_area:,.1f} km²",
            delta="Under monitoring"
        )
    
    with col2:
        st.metric(
            label="Protected Area", 
            value=f"{protected_area:,.1f} km²",
            delta=f"{protection_rate:.1%} coverage"
        )
    
    with col3:
        avg_protection = carbon_data["protection_effectiveness"].mean()
        st.metric(
            label="Policy Effectiveness", 
            value=f"{avg_protection:.1%}",
            delta="Improving trend"
        )
    
    with col4:
        st.metric(
            label="Compliance Rate", 
            value="94.2%",
            delta="Above target"
        )
    
    # Protection effectiveness by forest
    st.subheader("🛡️ Protection Effectiveness")
    protection_data = carbon_data.groupby("forest")["protection_effectiveness"].mean().reset_index()
    forest_status_data = pd.DataFrame({
        "forest": list(FOREST_LOCATIONS.keys()),
        "protection_status": [FOREST_LOCATIONS[f].get("protection_status", "Moderated Protected") for f in FOREST_LOCATIONS]
    })
    protection_data = protection_data.merge(forest_status_data, on="forest")
    
    fig_protection = px.bar(
        protection_data,
        x="forest",
        y="protection_effectiveness",
        color="protection_status",
        title="Protection Effectiveness by Forest",
        labels={"forest": "Forest", "protection_effectiveness": "Effectiveness Score"}
    )
    st.plotly_chart(fig_protection, width='stretch')
    
    # Policy recommendations
    st.subheader("💡 Policy Recommendations")
    recommendations = [
        "Increase ranger deployment in moderately protected areas",
        "Implement community-based forest monitoring programs",
        "Develop early warning systems for high-risk periods",
        "Establish buffer zones around critical forest areas",
        "Enhance penalties for illegal logging activities",
        "Create incentives for sustainable forest management"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

# Footer
st.markdown("---")
st.markdown("🌳 EcoGuard - Unified Forest Intelligence Platform")
st.markdown("All systems operational | Real-time monitoring and analytics")