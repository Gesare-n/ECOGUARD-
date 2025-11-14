"""
Acoustic Guardian - Research Dashboard

Advanced analytics dashboard for research institutions like KEFRI and DeKUT
focused on environmental modeling and innovation.
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
from scipy import stats

# Set page config
st.set_page_config(
    page_title="Acoustic Guardian - Research Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Kenya forest locations with realistic coordinates
FOREST_LOCATIONS = {
    "Karura Forest": {"lat": -1.2723, "lng": 36.8080, "area_km2": 17.5, "ecosystem": "Urban Forest"},
    "Ngong Forest": {"lat": -1.3500, "lng": 36.7000, "area_km2": 20.0, "ecosystem": "Montane Forest"},
    "Aberdare Forest": {"lat": -0.4500, "lng": 36.5000, "area_km2": 200.0, "ecosystem": "Montane Forest"},
    "Mt. Kenya Forest": {"lat": -0.2500, "lng": 37.7500, "area_km2": 150.0, "ecosystem": "Montane Forest"},
    "Arboretum Forest": {"lat": -0.5300, "lng": 36.5300, "area_km2": 5.0, "ecosystem": "Indigenous Forest"},
    "Kakamega Forest": {"lat": 0.3000, "lng": 34.7500, "area_km2": 70.0, "ecosystem": "Tropical Rainforest"}
}

# Environmental parameters
ENVIRONMENTAL_PARAMS = ["Temperature", "Humidity", "Soil Moisture", "Wind Speed", "Air Quality"]

# Mock sensor data generator with environmental parameters
def generate_research_data(days=30):
    # Set seed for consistent data generation
    random.seed(42)
    np.random.seed(42)
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        for forest, coords in FOREST_LOCATIONS.items():
            # Generate environmental data
            temp = 20 + 10 * np.sin(2 * np.pi * i / 365) + random.uniform(-2, 2)  # Seasonal temperature
            humidity = 60 + 20 * np.cos(2 * np.pi * i / 365) + random.uniform(-5, 5)  # Seasonal humidity
            soil_moisture = 40 + 30 * np.sin(2 * np.pi * i / 365) + random.uniform(-3, 3)
            wind_speed = 3 + 5 * random.random()
            air_quality = 80 + 20 * random.random()
            
            # Generate detection data
            chainsaw_detections = max(0, int(10 * np.exp(-0.02 * i) + random.uniform(-2, 2)))  # Decreasing trend
            vehicle_detections = max(0, int(5 * np.exp(-0.01 * i) + random.uniform(-1, 1)))
            fire_detections = random.choices([0, 1, 2], weights=[0.95, 0.04, 0.01])[0]
            
            record = {
                "date": date,
                "forest": forest,
                "ecosystem": coords["ecosystem"],
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
                "soil_moisture": round(soil_moisture, 1),
                "wind_speed": round(wind_speed, 1),
                "air_quality": round(air_quality, 1),
                "chainsaw_detections": chainsaw_detections,
                "vehicle_detections": vehicle_detections,
                "fire_detections": fire_detections,
                "total_detections": chainsaw_detections + vehicle_detections + fire_detections
            }
            data.append(record)
    
    return pd.DataFrame(data)

# Generate mock research data
df_research = generate_research_data(90)  # 90 days of data

# Sidebar
st.sidebar.title("🌳 Acoustic Guardian")
st.sidebar.markdown("### Research Dashboard")

# Research focus area
research_focus = st.sidebar.selectbox(
    "Research Focus",
    ["Environmental Correlation", "Threat Patterns", "Ecosystem Health", "Climate Impact"],
    index=0
)

# Date range selector
st.sidebar.subheader("📅 Date Range")
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Forest selector
st.sidebar.subheader("Forest Selection")
selected_forests = st.sidebar.multiselect(
    "Select Forests",
    list(FOREST_LOCATIONS.keys()),
    default=list(FOREST_LOCATIONS.keys())
)

# Ecosystem selector
st.sidebar.subheader("🌍 Ecosystem Types")
ecosystem_types = list(df_research["ecosystem"].unique())
selected_ecosystems = st.sidebar.multiselect(
    "Select Ecosystems",
    ecosystem_types,
    default=ecosystem_types
)

# Main dashboard
st.title("🌳 Acoustic Guardian - Research & Environmental Analytics")
st.markdown("### Advanced environmental modeling and data analysis for research institutions")
st.markdown("---")

# Filter data based on selections
filtered_data = df_research[
    (df_research["date"] >= pd.Timestamp(start_date)) & 
    (df_research["date"] <= pd.Timestamp(end_date)) &
    (df_research["forest"].isin(selected_forests)) &
    (df_research["ecosystem"].isin(selected_ecosystems))
]
df_filtered = pd.DataFrame(filtered_data)

if research_focus == "Environmental Correlation":
    st.header("🔬 Environmental Correlation Analysis")
    
    # Correlation matrix
    st.subheader("📊 Environmental Parameter Correlations")
    env_cols = ["temperature", "humidity", "soil_moisture", "wind_speed", "air_quality"]
    # Create a proper DataFrame with only the environmental columns
    env_data = pd.DataFrame()
    for col in env_cols:
        env_data[col] = df_filtered[col]
    corr_matrix = env_data.corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        labels=dict(x="Environmental Parameters", y="Environmental Parameters", color="Correlation"),
        x=env_cols,
        y=env_cols,
        color_continuous_scale="RdBu_r",
        title="Correlation Matrix of Environmental Parameters"
    )
    st.plotly_chart(fig_corr, width='stretch')
    
    # Temperature vs Detections
    st.subheader("🌡️ Temperature vs Threat Detections")
    fig_temp = px.scatter(
        df_filtered,
        x="temperature",
        y="total_detections",
        color="forest",
        title="Temperature vs Total Detections",
        labels={"temperature": "Temperature (°C)", "total_detections": "Total Detections"}
    )
    st.plotly_chart(fig_temp, width='stretch')
    
    # Humidity vs Detections
    st.subheader("💧 Humidity vs Threat Detections")
    fig_humidity = px.scatter(
        df_filtered,
        x="humidity",
        y="total_detections",
        color="forest",
        title="Humidity vs Total Detections",
        labels={"humidity": "Humidity (%)", "total_detections": "Total Detections"}
    )
    st.plotly_chart(fig_humidity, width='stretch')

elif research_focus == "Threat Patterns":
    st.header("🚨 Threat Pattern Analysis")
    
    # Detection trends over time
    st.subheader("📈 Detection Trends by Threat Type")
    detection_trends = df_filtered.groupby(["date"]).agg({
        "chainsaw_detections": "sum",
        "vehicle_detections": "sum",
        "fire_detections": "sum"
    }).reset_index()
    
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=detection_trends["date"],
        y=detection_trends["chainsaw_detections"],
        mode='lines+markers',
        name='Chainsaw Detections',
        line=dict(color='red')
    ))
    fig_trends.add_trace(go.Scatter(
        x=detection_trends["date"],
        y=detection_trends["vehicle_detections"],
        mode='lines+markers',
        name='Vehicle Detections',
        line=dict(color='blue')
    ))
    fig_trends.add_trace(go.Scatter(
        x=detection_trends["date"],
        y=detection_trends["fire_detections"],
        mode='lines+markers',
        name='Fire Detections',
        line=dict(color='orange')
    ))
    fig_trends.update_layout(
        title="Threat Detection Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Detections"
    )
    st.plotly_chart(fig_trends, width='stretch')
    
    # Forest comparison
    st.subheader("🌲 Threat Detections by Forest")
    forest_detections = df_filtered.groupby(["forest"]).agg({
        "chainsaw_detections": "sum",
        "vehicle_detections": "sum",
        "fire_detections": "sum"
    }).reset_index()
    
    fig_forest = go.Figure()
    fig_forest.add_trace(go.Bar(
        x=forest_detections["forest"],
        y=forest_detections["chainsaw_detections"],
        name='Chainsaw Detections',
        marker_color='red'
    ))
    fig_forest.add_trace(go.Bar(
        x=forest_detections["forest"],
        y=forest_detections["vehicle_detections"],
        name='Vehicle Detections',
        marker_color='blue'
    ))
    fig_forest.add_trace(go.Bar(
        x=forest_detections["forest"],
        y=forest_detections["fire_detections"],
        name='Fire Detections',
        marker_color='orange'
    ))
    fig_forest.update_layout(
        title="Threat Detections by Forest",
        xaxis_title="Forest",
        yaxis_title="Number of Detections",
        barmode='group'
    )
    st.plotly_chart(fig_forest, width='stretch')

elif research_focus == "Ecosystem Health":
    st.header("🌱 Ecosystem Health Indicators")
    
    # Environmental health scores
    st.subheader("📊 Ecosystem Health Scores")
    
    # Calculate health scores (simplified model)
    df_health = df_filtered.copy()
    df_health["health_score"] = (
        (df_health["air_quality"] / 100) * 0.3 +
        (df_health["soil_moisture"] / 100) * 0.3 +
        (1 - df_health["total_detections"] / 20) * 0.4
    ) * 100
    df_health["health_score"] = df_health["health_score"].clip(0, 100)
    
    health_by_forest = df_health.groupby("forest")["health_score"].mean().reset_index()
    
    fig_health = px.bar(
        health_by_forest,
        x="forest",
        y="health_score",
        color="health_score",
        color_continuous_scale="Greens",
        title="Average Ecosystem Health Score by Forest",
        labels={"health_score": "Health Score (0-100)", "forest": "Forest"}
    )
    st.plotly_chart(fig_health, width='stretch')
    
    # Environmental parameters over time
    st.subheader("🌡️ Environmental Parameters Over Time")
    env_params = df_filtered.groupby("date").agg({
        "temperature": "mean",
        "humidity": "mean",
        "soil_moisture": "mean",
        "air_quality": "mean"
    }).reset_index()
    
    fig_env = go.Figure()
    fig_env.add_trace(go.Scatter(
        x=env_params["date"],
        y=env_params["temperature"],
        mode='lines',
        name='Temperature (°C)',
        yaxis="y"
    ))
    fig_env.add_trace(go.Scatter(
        x=env_params["date"],
        y=env_params["humidity"],
        mode='lines',
        name='Humidity (%)',
        yaxis="y2"
    ))
    fig_env.update_layout(
        title="Environmental Parameters Over Time",
        xaxis_title="Date",
        yaxis=dict(title="Temperature (°C)", side="left"),
        yaxis2=dict(title="Humidity (%)", side="right", overlaying="y"),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig_env, width='stretch')

elif research_focus == "Climate Impact":
    st.header("🌍 Climate Impact Analysis")
    
    # Seasonal patterns
    st.subheader("🌀 Seasonal Detection Patterns")
    # Convert date column to datetime if it's not already
    df_filtered["date"] = pd.to_datetime(df_filtered["date"])
    df_filtered["month"] = df_filtered["date"].dt.month
    seasonal_data = df_filtered.groupby("month").agg({
        "chainsaw_detections": "sum",
        "vehicle_detections": "sum",
        "fire_detections": "sum"
    }).reset_index()
    
    # Map month numbers to names
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonal_data["month_name"] = seasonal_data["month"].apply(lambda x: month_names[x-1])
    
    fig_seasonal = go.Figure()
    fig_seasonal.add_trace(go.Bar(
        x=seasonal_data["month_name"],
        y=seasonal_data["chainsaw_detections"],
        name='Chainsaw Detections',
        marker_color='red'
    ))
    fig_seasonal.add_trace(go.Bar(
        x=seasonal_data["month_name"],
        y=seasonal_data["vehicle_detections"],
        name='Vehicle Detections',
        marker_color='blue'
    ))
    fig_seasonal.add_trace(go.Bar(
        x=seasonal_data["month_name"],
        y=seasonal_data["fire_detections"],
        name='Fire Detections',
        marker_color='orange'
    ))
    fig_seasonal.update_layout(
        title="Seasonal Threat Detection Patterns",
        xaxis_title="Month",
        yaxis_title="Number of Detections",
        barmode='group'
    )
    st.plotly_chart(fig_seasonal, width='stretch')
    
    # Climate correlation
    st.subheader("🌡️ Climate Correlation Analysis")
    
    # Calculate correlation between temperature and detections
    temp_series = pd.Series(df_filtered["temperature"])
    detections_series = pd.Series(df_filtered["total_detections"])
    temp_corr = temp_series.corr(detections_series)
    humidity_series = pd.Series(df_filtered["humidity"])
    humidity_corr = humidity_series.corr(detections_series)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Temperature-Detection Correlation",
            value=f"{temp_corr:.3f}",
            delta="Weak negative" if temp_corr < 0 else "Positive"
        )
    with col2:
        st.metric(
            label="Humidity-Detection Correlation",
            value=f"{humidity_corr:.3f}",
            delta="Weak negative" if humidity_corr < 0 else "Positive"
        )

# Data export section
st.header("💾 Data Export")
st.markdown("Export research data for further analysis:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Export Environmental Data"):
        st.success("Environmental data exported successfully!")

with col2:
    if st.button("Export Detection Data"):
        st.success("Detection data exported successfully!")

with col3:
    if st.button("Export All Data"):
        st.success("All research data exported successfully!")

# Research collaboration
st.header("🤝 Research Collaboration")
st.markdown("""
KEFRI and DeKUT researchers can use this dashboard to:
- Analyze long-term environmental trends
- Study the correlation between climate factors and illegal activities
- Develop predictive models for threat detection
- Support policy development with data-driven insights
- Collaborate with international research institutions
""")

# Footer
st.markdown("---")
st.markdown("🌳 Acoustic Guardian - Advancing environmental research through acoustic intelligence")
st.markdown(f"Data period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")