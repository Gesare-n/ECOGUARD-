"""
EcoGuard - Deforestation Analysis Dashboard

This dashboard provides in-depth analysis of deforestation patterns with a focus on
Nairobi's forest areas and data-driven insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="EcoGuard - Deforestation Analysis",
    page_icon="🌳",
    layout="wide"
)

# Deforestation data for Nairobi region (mock data with realistic patterns)
DEFORESTATION_DATA = [
    # Karura Forest data
    {"year": 2015, "area_hectares": 1200, "location": "Karura Forest", "cause": "Urban Expansion", "coordinates": "-1.2723, 36.8080"},
    {"year": 2016, "area_hectares": 950, "location": "Karura Forest", "cause": "Illegal Logging", "coordinates": "-1.2723, 36.8080"},
    {"year": 2017, "area_hectares": 780, "location": "Karura Forest", "cause": "Agriculture", "coordinates": "-1.2723, 36.8080"},
    {"year": 2018, "area_hectares": 620, "location": "Karura Forest", "cause": "Infrastructure", "coordinates": "-1.2723, 36.8080"},
    {"year": 2019, "area_hectares": 510, "location": "Karura Forest", "cause": "Urban Expansion", "coordinates": "-1.2723, 36.8080"},
    {"year": 2020, "area_hectares": 430, "location": "Karura Forest", "cause": "Illegal Logging", "coordinates": "-1.2723, 36.8080"},
    {"year": 2021, "area_hectares": 320, "location": "Karura Forest", "cause": "Agriculture", "coordinates": "-1.2723, 36.8080"},
    {"year": 2022, "area_hectares": 210, "location": "Karura Forest", "cause": "Conservation Efforts", "coordinates": "-1.2723, 36.8080"},
    {"year": 2023, "area_hectares": 150, "location": "Karura Forest", "cause": "Conservation Efforts", "coordinates": "-1.2723, 36.8080"},
    {"year": 2024, "area_hectares": 90, "location": "Karura Forest", "cause": "Conservation Efforts", "coordinates": "-1.2723, 36.8080"},
    
    # Ngong Forest data
    {"year": 2015, "area_hectares": 800, "location": "Ngong Forest", "cause": "Urban Expansion", "coordinates": "-1.3500, 36.7000"},
    {"year": 2016, "area_hectares": 720, "location": "Ngong Forest", "cause": "Charcoal Production", "coordinates": "-1.3500, 36.7000"},
    {"year": 2017, "area_hectares": 650, "location": "Ngong Forest", "cause": "Agriculture", "coordinates": "-1.3500, 36.7000"},
    {"year": 2018, "area_hectares": 580, "location": "Ngong Forest", "cause": "Settlements", "coordinates": "-1.3500, 36.7000"},
    {"year": 2019, "area_hectares": 490, "location": "Ngong Forest", "cause": "Urban Expansion", "coordinates": "-1.3500, 36.7000"},
    {"year": 2020, "area_hectares": 410, "location": "Ngong Forest", "cause": "Charcoal Production", "coordinates": "-1.3500, 36.7000"},
    {"year": 2021, "area_hectares": 330, "location": "Ngong Forest", "cause": "Agriculture", "coordinates": "-1.3500, 36.7000"},
    {"year": 2022, "area_hectares": 260, "location": "Ngong Forest", "cause": "Conservation Efforts", "coordinates": "-1.3500, 36.7000"},
    {"year": 2023, "area_hectares": 180, "location": "Ngong Forest", "cause": "Conservation Efforts", "coordinates": "-1.3500, 36.7000"},
    {"year": 2024, "area_hectares": 120, "location": "Ngong Forest", "cause": "Conservation Efforts", "coordinates": "-1.3500, 36.7000"},
    
    # Aberdare Forest data
    {"year": 2015, "area_hectares": 2500, "location": "Aberdare Forest", "cause": "Illegal Logging", "coordinates": "-0.4500, 36.5000"},
    {"year": 2016, "area_hectares": 2300, "location": "Aberdare Forest", "cause": "Charcoal Production", "coordinates": "-0.4500, 36.5000"},
    {"year": 2017, "area_hectares": 2100, "location": "Aberdare Forest", "cause": "Agriculture", "coordinates": "-0.4500, 36.5000"},
    {"year": 2018, "area_hectares": 1900, "location": "Aberdare Forest", "cause": "Settlements", "coordinates": "-0.4500, 36.5000"},
    {"year": 2019, "area_hectares": 1700, "location": "Aberdare Forest", "cause": "Illegal Logging", "coordinates": "-0.4500, 36.5000"},
    {"year": 2020, "area_hectares": 1500, "location": "Aberdare Forest", "cause": "Charcoal Production", "coordinates": "-0.4500, 36.5000"},
    {"year": 2021, "area_hectares": 1300, "location": "Aberdare Forest", "cause": "Agriculture", "coordinates": "-0.4500, 36.5000"},
    {"year": 2022, "area_hectares": 1100, "location": "Aberdare Forest", "cause": "Conservation Efforts", "coordinates": "-0.4500, 36.5000"},
    {"year": 2023, "area_hectares": 900, "location": "Aberdare Forest", "cause": "Conservation Efforts", "coordinates": "-0.4500, 36.5000"},
    {"year": 2024, "area_hectares": 700, "location": "Aberdare Forest", "cause": "Conservation Efforts", "coordinates": "-0.4500, 36.5000"}
]

# Forest characteristics data
FOREST_INFO = {
    "Karura Forest": {
        "area_km2": 17.5,
        "established": 1999,
        "protected_status": "Urban Forest Reserve",
        "biodiversity": "Over 150 bird species, 20 mammal species",
        "significance": "Largest urban forest in Nairobi"
    },
    "Ngong Forest": {
        "area_km2": 20.0,
        "established": 1935,
        "protected_status": "Forest Reserve",
        "biodiversity": "Home to elands, bushbucks, and over 100 bird species",
        "significance": "Important water catchment area"
    },
    "Aberdare Forest": {
        "area_km2": 200.0,
        "established": 1950,
        "protected_status": "National Park",
        "biodiversity": "Black rhinos, elephants, leopards, over 250 bird species",
        "significance": "Critical water tower for Nairobi"
    }
}

# Sidebar
st.sidebar.title("🌳 EcoGuard")
st.sidebar.markdown("### Deforestation Analysis")

# Analysis type selector
analysis_type = st.sidebar.radio(
    "Analysis Type",
    ["Overview", "Trend Analysis", "Cause Analysis", "Forest Comparison"],
    index=0
)

# Date range selector
st.sidebar.subheader("📅 Date Range")
start_year = st.sidebar.slider("Start Year", 2015, 2024, 2015)
end_year = st.sidebar.slider("End Year", 2015, 2024, 2024)

# Forest selector
st.sidebar.subheader("Forest Selection")
selected_forests = st.sidebar.multiselect(
    "Select Forests",
    ["Karura Forest", "Ngong Forest", "Aberdare Forest"],
    default=["Karura Forest", "Ngong Forest", "Aberdare Forest"]
)

# Main dashboard
st.title("🌳 EcoGuard - Deforestation Analysis Dashboard")
st.markdown("### Data-driven insights into forest loss and conservation efforts in Nairobi")

# Filter data based on selections
df = pd.DataFrame(DEFORESTATION_DATA)
df_filtered = df[
    (df["year"] >= start_year) & 
    (df["year"] <= end_year) & 
    (df["location"].isin(selected_forests))
]

if analysis_type == "Overview":
    # Overview section
    st.header("📊 Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_deforestation = df_filtered["area_hectares"].sum()
    avg_annual_loss = total_deforestation / (end_year - start_year + 1)
    
    with col1:
        st.metric(
            label="Total Deforestation", 
            value=f"{total_deforestation:,.0f} ha",
            delta=f"{avg_annual_loss:.0f} ha/year avg"
        )
    
    with col2:
        st.metric(
            label="Affected Forests", 
            value=len(selected_forests),
            delta="Selected"
        )
    
    with col3:
        st.metric(
            label="Analysis Period", 
            value=f"{end_year - start_year + 1} years",
            delta=f"{start_year}-{end_year}"
        )
    
    with col4:
        # Calculate conservation improvement
        early_period = df_filtered[df_filtered["year"] <= (start_year + end_year) // 2]["area_hectares"].sum()
        late_period = df_filtered[df_filtered["year"] > (start_year + end_year) // 2]["area_hectares"].sum()
        improvement = ((early_period - late_period) / early_period * 100) if early_period > 0 else 0
        
        st.metric(
            label="Conservation Impact", 
            value=f"{improvement:.0f}%",
            delta="Improvement" if improvement > 0 else "Concern"
        )
    
    # Deforestation trend chart
    st.subheader("📈 Deforestation Trend Over Time")
    fig_trend = px.line(
        df_filtered.groupby("year")["area_hectares"].sum().reset_index(),
        x="year",
        y="area_hectares",
        title="Annual Deforestation Trend",
        labels={"year": "Year", "area_hectares": "Area Deforested (Hectares)"},
        markers=True
    )
    fig_trend.update_layout(hovermode="x")
    st.plotly_chart(fig_trend, width='stretch')
    
    # Forest comparison
    st.subheader("🌲 Forest Comparison")
    fig_forest = px.bar(
        df_filtered.groupby("location")["area_hectares"].sum().reset_index(),
        x="location",
        y="area_hectares",
        color="location",
        title="Total Deforestation by Forest",
        labels={"location": "Forest", "area_hectares": "Area Deforested (Hectares)"}
    )
    st.plotly_chart(fig_forest, width='stretch')
    
    # Forest information cards
    st.subheader("ℹ️ Forest Information")
    cols = st.columns(len(selected_forests))
    
    for i, forest in enumerate(selected_forests):
        with cols[i]:
            info = FOREST_INFO[forest]
            st.markdown(f"### {forest}")
            st.markdown(f"**Area:** {info['area_km2']} km²")
            st.markdown(f"**Established:** {info['established']}")
            st.markdown(f"**Status:** {info['protected_status']}")
            st.markdown(f"**Biodiversity:** {info['biodiversity']}")
            st.markdown(f"**Significance:** {info['significance']}")

elif analysis_type == "Trend Analysis":
    st.header("📈 Trend Analysis")
    
    # Year-over-year change
    st.subheader("🔄 Year-over-Year Change")
    yearly_data = df_filtered.groupby("year")["area_hectares"].sum().reset_index()
    yearly_data["yoy_change"] = yearly_data["area_hectares"].pct_change() * 100
    
    fig_yoy = px.bar(
        yearly_data,
        x="year",
        y="yoy_change",
        title="Year-over-Year Change in Deforestation",
        labels={"year": "Year", "yoy_change": "Change (%)"}
    )
    fig_yoy.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_yoy, width='stretch')
    
    # Moving average trend
    st.subheader("📉 Moving Average Trend")
    yearly_data["ma_3year"] = yearly_data["area_hectares"].rolling(window=3).mean()
    
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(
        x=yearly_data["year"],
        y=yearly_data["area_hectares"],
        mode='lines+markers',
        name='Annual Deforestation',
        line=dict(color='blue')
    ))
    fig_ma.add_trace(go.Scatter(
        x=yearly_data["year"],
        y=yearly_data["ma_3year"],
        mode='lines',
        name='3-Year Moving Average',
        line=dict(color='red', width=3)
    ))
    fig_ma.update_layout(
        title="Deforestation with 3-Year Moving Average",
        xaxis_title="Year",
        yaxis_title="Area Deforested (Hectares)"
    )
    st.plotly_chart(fig_ma, width='stretch')

elif analysis_type == "Cause Analysis":
    st.header("🔍 Cause Analysis")
    
    # Deforestation by cause
    st.subheader("🏭 Deforestation Causes")
    cause_data = df_filtered.groupby("cause")["area_hectares"].sum().reset_index()
    cause_data = cause_data.sort_values("area_hectares", ascending=False)
    
    fig_cause = px.pie(
        cause_data,
        values="area_hectares",
        names="cause",
        title="Deforestation by Cause",
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    st.plotly_chart(fig_cause, width='stretch')
    
    # Cause trend over time
    st.subheader("📅 Causes Over Time")
    cause_trend = df_filtered.groupby(["year", "cause"])["area_hectares"].sum().reset_index()
    
    fig_cause_trend = px.area(
        cause_trend,
        x="year",
        y="area_hectares",
        color="cause",
        title="Deforestation Causes Over Time"
    )
    st.plotly_chart(fig_cause_trend, width='stretch')
    
    # Cause comparison by forest
    st.subheader("🌲 Causes by Forest")
    cause_forest = df_filtered.groupby(["location", "cause"])["area_hectares"].sum().reset_index()
    
    fig_cause_forest = px.bar(
        cause_forest,
        x="location",
        y="area_hectares",
        color="cause",
        title="Deforestation Causes by Forest",
        labels={"location": "Forest", "area_hectares": "Area Deforested (Hectares)"}
    )
    st.plotly_chart(fig_cause_forest, width='stretch')

elif analysis_type == "Forest Comparison":
    st.header("🌲 Forest Comparison")
    
    # Size comparison
    st.subheader("📏 Forest Size Comparison")
    forest_sizes = []
    for forest in selected_forests:
        forest_sizes.append({
            "forest": forest,
            "size_km2": FOREST_INFO[forest]["area_km2"]
        })
    
    df_sizes = pd.DataFrame(forest_sizes)
    fig_size = px.bar(
        df_sizes,
        x="forest",
        y="size_km2",
        color="forest",
        title="Forest Size Comparison",
        labels={"forest": "Forest", "size_km2": "Area (km²)"}
    )
    st.plotly_chart(fig_size, width='stretch')
    
    # Deforestation rate comparison
    st.subheader("📉 Deforestation Rate Comparison")
    forest_deforest = df_filtered.groupby("location")["area_hectares"].sum().reset_index()
    forest_deforest = forest_deforest.merge(df_sizes, left_on="location", right_on="forest")
    forest_deforest["rate_per_km2"] = forest_deforest["area_hectares"] / forest_deforest["size_km2"]
    
    fig_rate = px.bar(
        forest_deforest,
        x="location",
        y="rate_per_km2",
        color="location",
        title="Deforestation Rate (ha/km²)",
        labels={"location": "Forest", "rate_per_km2": "Deforestation Rate (ha/km²)"}
    )
    st.plotly_chart(fig_rate, width='stretch')
    
    # Biodiversity impact
    st.subheader("🐾 Biodiversity Significance")
    biodiversity_data = []
    for forest in selected_forests:
        biodiversity_data.append({
            "forest": forest,
            "significance": FOREST_INFO[forest]["significance"],
            "biodiversity": FOREST_INFO[forest]["biodiversity"]
        })
    
    for item in biodiversity_data:
        st.markdown(f"### {item['forest']}")
        st.markdown(f"**Significance:** {item['significance']}")
        st.markdown(f"**Biodiversity:** {item['biodiversity']}")
        st.markdown("---")

# Data table
st.header("📋 Detailed Data")
df_display = pd.DataFrame()
df_display["Year"] = df_filtered["year"]
df_display["Forest"] = df_filtered["location"]
df_display["Area Affected (ha)"] = df_filtered["area_hectares"]
df_display["Primary Cause"] = df_filtered["cause"]
st.dataframe(
    df_display,
    width='stretch'
)

# Footer
st.markdown("---")
st.markdown("🌳 EcoGuard - Providing data-driven insights for forest conservation")
st.markdown("Data sources: Mock data based on realistic deforestation patterns in Nairobi")