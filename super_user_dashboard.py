import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
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
    page_title="EcoGuard - Super User Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

# Sidebar Navigation
st.sidebar.title("🌳 EcoGuard")
st.sidebar.markdown("### Super User Control Center")

# Navigation menu
navigation_options = {
    "Overview": "🏠 Overview",
    "Main Dashboard": "🖥️ Main System",
    "Nairobi Dashboard": "🌳 Nairobi Forests",
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
    st.title("🌳 EcoGuard - Super User Dashboard")
    st.markdown("### Centralized Forest Intelligence Platform for Kenya")
    
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
    
    # System Overview
    st.header("🌍 Comprehensive Forest Intelligence Overview")
    
    # Key metrics across all systems
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Forests", 
            value=len(FOREST_LOCATIONS), 
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
        total_area = sum([coords["area_km2"] for coords in FOREST_LOCATIONS.values()])
        st.metric(
            label="Protected Area", 
            value=f"{total_area:.1f} km²",
            delta="↑ 12 km² conserved"
        )
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌳 Forest Overview", "🌱 Reforestation Areas", "🔥 Deforestation Impact", "📡 Sensor Priority Map", "🌿 Nursery Monitoring"])

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
        st.subheader("🌱 Newly Planted Reforestation Areas")
        
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
        st.subheader("📈 Reforestation Progress")
        reforestation_df = pd.DataFrame(reforestation_data)
        st.dataframe(reforestation_df, width='stretch')
        
        total_hectares = sum([area["hectares"] for area in reforestation_data])
        total_trees = sum([area["trees_planted"] for area in reforestation_data])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Reforested Area", f"{total_hectares} hectares")
        with col2:
            st.metric("Total Trees Planted", f"{total_trees:,}")
    
    with tab3:
        st.subheader("🔥 Areas Affected by Deforestation")
        
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
    
    with tab4:
        st.subheader("📡 Priority Areas for Sensor Deployment")
        
        # Create map with risk assessment and sensor placement recommendations with Google Maps
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
        
        # Add legend
        legend_html = '''
         <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 150px; height: 120px; 
         background-color: white; border:2px solid grey; z-index:9999; 
         font-size:14px; padding: 10px">
         <p><strong>Sensor Priority Legend</strong></p>
         <p><i class="fa fa-map-marker" style="color:red"></i> High Priority</p>
         <p><i class="fa fa-map-marker" style="color:orange"></i> Medium Priority</p>
         <p><i class="fa fa-map-marker" style="color:green"></i> Low Priority</p>
         </div>
         '''
        m4.get_root().html.add_child(folium.Element(legend_html))
        
        # Display map
        st_folium(m4, width=700, height=500)
        
        # Risk assessment table
        st.subheader("📊 Risk Assessment and Sensor Recommendations")
        if not risk_data.empty:
            # Merge risk data with forest data
            risk_assessment = risk_data.merge(forest_data, left_on="forest", right_on="name")
            risk_assessment["recommended_sensors"] = risk_assessment.apply(
                lambda row: max(1, int(row["area_km2"] / 50 * (row["risk_score"] * 2))), axis=1
            )
            
            # Sort by risk score
            risk_assessment = risk_assessment.sort_values("risk_score", ascending=False)
            
            st.dataframe(risk_assessment[["forest", "risk_score", "urban_proximity", "accessibility", "historical_loss", "recommended_sensors"]], width='stretch')
        else:
            st.info("No risk assessment data available.")
    
    with tab5:
        st.subheader("🌿 Nursery Monitoring and Reforestation Sites")
        
        # Mock nursery and reforestation monitoring data
        nursery_data = [
            {"name": "Karura Forest Nursery", "lat": -1.2700, "lng": 36.8100, "seedlings": 5000, "species": "Indigenous Trees", "status": "Healthy", "last_review": "2024-05-15", "next_review": "2024-06-15"},
            {"name": "Ngong Forest Seed Bank", "lat": -1.3400, "lng": 36.6900, "seedlings": 12000, "species": "Acacia, Croton", "status": "Needs Attention", "last_review": "2024-04-22", "next_review": "2024-05-22"},
            {"name": "Aberdare Reforestation Hub", "lat": -0.4400, "lng": 36.4900, "seedlings": 8500, "species": "Oak, Cedar", "status": "Healthy", "last_review": "2024-05-10", "next_review": "2024-06-10"},
            {"name": "Kakamega Tree Farm", "lat": 0.2900, "lng": 34.7400, "seedlings": 6200, "species": "Indigenous Shade Trees", "status": "Excellent", "last_review": "2024-05-18", "next_review": "2024-06-18"},
            {"name": "Mau Forest Greenhouse", "lat": -0.4900, "lng": 35.4900, "seedlings": 15000, "species": "Various Native Species", "status": "Critical", "last_review": "2024-03-30", "next_review": "2024-05-30"}
        ]
        
        # Create map for nursery locations
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
    st.markdown("🌳 EcoGuard - Unified Forest Intelligence Platform")
    st.markdown("Super User Access | All Systems Operational")

elif current_page == "Main Dashboard":
    # Display content from the main dashboard
    st.title("🖥️ Main System Dashboard")
    st.markdown("### Core EcoGuard Monitoring System")
    
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
        tooltip="EcoGuard Sensor",
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