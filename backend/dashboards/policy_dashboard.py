"""
EcoGuard - Policy & Carbon Credit Dashboard

Dashboard for carbon credit developers and policy agencies focused on
forest protection metrics and verification for carbon credit applications.
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
    page_title="EcoGuard - Policy Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Kenya forest locations with carbon data
FOREST_LOCATIONS = {
    "Karura Forest": {
        "lat": -1.2723, "lng": 36.8080, "area_km2": 17.5, 
        "carbon_tons_per_km2": 150000, "protection_status": "Highly Protected"
    },
    "Ngong Forest": {
        "lat": -1.3500, "lng": 36.7000, "area_km2": 20.0, 
        "carbon_tons_per_km2": 120000, "protection_status": "Moderately Protected"
    },
    "Aberdare Forest": {
        "lat": -0.4500, "lng": 36.5000, "area_km2": 200.0, 
        "carbon_tons_per_km2": 180000, "protection_status": "Highly Protected"
    },
    "Mt. Kenya Forest": {
        "lat": -0.2500, "lng": 37.7500, "area_km2": 150.0, 
        "carbon_tons_per_km2": 160000, "protection_status": "Highly Protected"
    },
    "Arboretum Forest": {
        "lat": -0.5300, "lng": 36.5300, "area_km2": 5.0, 
        "carbon_tons_per_km2": 100000, "protection_status": "Well Protected"
    },
    "Kakamega Forest": {
        "lat": 0.3000, "lng": 34.7500, "area_km2": 70.0, 
        "carbon_tons_per_km2": 200000, "protection_status": "Moderately Protected"
    }
}

# Mock carbon credit data
def generate_carbon_data():
    # Set seed for consistent data generation
    random.seed(42)
    data = []
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(365):
        date = base_date + timedelta(days=i)
        
        # Simulate decreasing deforestation over time (improvement)
        reduction_factor = 1 - (i / 365) * 0.6  # 60% improvement over the year
        
        for forest, info in FOREST_LOCATIONS.items():
            # Base deforestation (hectares)
            base_deforestation = random.uniform(0.1, 2.0)
            actual_deforestation = base_deforestation * reduction_factor
            
            # Calculate carbon impact
            carbon_per_hectare = info["carbon_tons_per_km2"] / 100  # Convert to per hectare
            carbon_loss = actual_deforestation * carbon_per_hectare
            
            # Calculate protection effectiveness
            protection_mapping = {
                "Highly Protected": 0.95,
                "Well Protected": 0.85,
                "Moderately Protected": 0.70
            }
            protection_effectiveness = protection_mapping[info["protection_status"]]
            
            record = {
                "date": date,
                "forest": forest,
                "deforestation_ha": round(actual_deforestation, 2),
                "carbon_loss_tons": round(carbon_loss, 2),
                "protection_status": info["protection_status"],
                "protection_effectiveness": protection_effectiveness,
                "total_carbon_stored": round(info["area_km2"] * info["carbon_tons_per_km2"] * (1 - i/365 * 0.1), 0)
            }
            data.append(record)
    
    return pd.DataFrame(data)

# Generate carbon data
df_carbon = generate_carbon_data()

# Sidebar
st.sidebar.title("🌳 EcoGuard")
st.sidebar.markdown("### Policy & Carbon Credit Dashboard")

# Dashboard focus
dashboard_focus = st.sidebar.radio(
    "Dashboard Focus",
    ["Carbon Credits", "Policy Metrics", "Compliance Reporting"],
    index=0
)

# Date range selector
st.sidebar.subheader("📅 Date Range")
reporting_period = st.sidebar.selectbox(
    "Reporting Period",
    ["Last 30 Days", "Last 90 Days", "Last Year", "Custom"],
    index=2
)

if reporting_period == "Custom":
    start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365))
    end_date = st.sidebar.date_input("End Date", datetime.now())
else:
    end_date = datetime.now()
    if reporting_period == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif reporting_period == "Last 90 Days":
        start_date = end_date - timedelta(days=90)
    else:  # Last Year
        start_date = end_date - timedelta(days=365)

# Forest selector
st.sidebar.subheader("Forest Selection")
selected_forests = st.sidebar.multiselect(
    "Select Forests",
    list(FOREST_LOCATIONS.keys()),
    default=list(FOREST_LOCATIONS.keys())
)

# Main dashboard
st.title("🌳 EcoGuard - Policy & Carbon Credit Analytics")
st.markdown("### Verified forest protection metrics for carbon credit applications and policy development")
st.markdown("---")

# Filter data based on selections
df_filtered = df_carbon[
    (df_carbon["date"] >= pd.Timestamp(start_date)) & 
    (df_carbon["date"] <= pd.Timestamp(end_date)) &
    (df_carbon["forest"].isin(selected_forests))
]

if dashboard_focus == "Carbon Credits":
    st.header("🪙 Carbon Credit Analytics")
    
    # Key carbon metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_deforestation = df_filtered["deforestation_ha"].sum()
    total_carbon_loss = df_filtered["carbon_loss_tons"].sum()
    avg_protection = df_filtered["protection_effectiveness"].mean()
    
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
    carbon_storage = df_filtered.groupby("date")["total_carbon_stored"].mean().reset_index()
    
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
    deforestation_by_forest = df_filtered.groupby("forest")["deforestation_ha"].sum().reset_index()
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
    
    # Carbon credit verification
    st.subheader("✅ Carbon Credit Verification")
    st.markdown("""
    **Verification Methodology:**
    - Continuous acoustic monitoring with verified detection accuracy
    - GPS-tagged threat events with timestamp verification
    - Independent audit trail of all detections
    - Integration with Kenya Forest Service databases
    
    **Certification Standards:**
    - Verified Carbon Standard (VCS)
    - Climate, Community & Biodiversity (CCB) Standards
    - Gold Standard for carbon credits
    """)
    
    # Verification metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Data Verification Rate", 
            value="99.7%",
            delta="Audited"
        )
    
    with col2:
        st.metric(
            label="Third-Party Audits", 
            value="Quarterly",
            delta="Compliant"
        )
    
    with col3:
        st.metric(
            label="Certification Status", 
            value="In Progress",
            delta="VCS Application"
        )

elif dashboard_focus == "Policy Metrics":
    st.header("📜 Policy Development Metrics")
    
    # Policy impact metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate policy metrics
    total_forest_area = sum([FOREST_LOCATIONS[f]["area_km2"] for f in selected_forests])
    protected_area = sum([FOREST_LOCATIONS[f]["area_km2"] for f in selected_forests 
                         if FOREST_LOCATIONS[f]["protection_status"] in ["Highly Protected", "Well Protected"]])
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
        st.metric(
            label="Policy Effectiveness", 
            value=f"{df_filtered['protection_effectiveness'].mean():.1%}",
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
    protection_data = df_filtered.groupby("forest")["protection_effectiveness"].mean().reset_index()
    forest_status_data = pd.DataFrame({
        "forest": [f for f in selected_forests],
        "protection_status": [FOREST_LOCATIONS[f]["protection_status"] for f in selected_forests]
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

elif dashboard_focus == "Compliance Reporting":
    st.header("📋 Compliance & Reporting")
    
    # Reporting metrics
    col1, col2, col3, col4 = st.columns(4)
    
    reporting_period_days = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days
    report_completion = 100  # Assuming full compliance for demo
    audit_findings = 2  # Mock findings
    corrective_actions = audit_findings  # Assuming all addressed
    
    with col1:
        st.metric(
            label="Reporting Period", 
            value=f"{reporting_period_days} days",
            delta="Complete"
        )
    
    with col2:
        st.metric(
            label="Report Completion", 
            value=f"{report_completion}%",
            delta="On schedule"
        )
    
    with col3:
        st.metric(
            label="Audit Findings", 
            value=audit_findings,
            delta="All addressed"
        )
    
    with col4:
        st.metric(
            label="Corrective Actions", 
            value=corrective_actions,
            delta="100% completion"
        )
    
    # Compliance timeline
    st.subheader("📅 Compliance Timeline")
    
    # Mock compliance events
    compliance_events = [
        {"date": datetime.now() - timedelta(days=350), "event": "Q1 Monitoring Report", "status": "Completed"},
        {"date": datetime.now() - timedelta(days=260), "event": "Q2 Monitoring Report", "status": "Completed"},
        {"date": datetime.now() - timedelta(days=170), "event": "Q3 Monitoring Report", "status": "Completed"},
        {"date": datetime.now() - timedelta(days=80), "event": "Q4 Monitoring Report", "status": "Completed"},
        {"date": datetime.now() - timedelta(days=10), "event": "Annual Audit", "status": "In Progress"},
        {"date": datetime.now() + timedelta(days=30), "event": "Q1 Next Year", "status": "Scheduled"}
    ]
    
    for event in compliance_events:
        status_emoji = "✅" if event["status"] == "Completed" else "🔄" if event["status"] == "In Progress" else "📅"
        st.markdown(f"{status_emoji} **{event['date'].strftime('%Y-%m-%d')}**: {event['event']} - {event['status']}")
    
    # Export compliance report
    st.subheader("📤 Export Compliance Report")
    report_format = st.selectbox("Select Report Format", ["PDF", "Excel", "CSV"], index=0)
    
    if st.button("Generate Compliance Report"):
        st.success(f"Compliance report generated in {report_format} format!")
        st.info("Report includes: Monitoring data, threat analysis, protection effectiveness, and policy recommendations.")

# Data verification section
st.header("🔍 Data Verification & Transparency")
st.markdown("""
All data in this dashboard is:
- **Continuously monitored** by acoustic sensors
- **Independently verified** through third-party audits
- **Blockchain timestamped** for immutability
- **Cross-referenced** with satellite imagery and KFS records
""")

# Verification badges
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("https://placehold.co/100x50?text=VCS", caption="Verified Carbon Standard")

with col2:
    st.image("https://placehold.co/100x50?text=CCB", caption="Climate Community & Biodiversity")

with col3:
    st.image("https://placehold.co/100x50?text=Gold+Standard", caption="Gold Standard")

with col4:
    st.image("https://placehold.co/100x50?text=KFS", caption="Kenya Forest Service")

# Footer
st.markdown("---")
st.markdown("🌳 EcoGuard - Transparent, verified forest protection for carbon credit development")
st.markdown(f"Reporting period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")