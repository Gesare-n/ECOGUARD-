"""
Acoustic Guardian - Streamlit Dashboard Demo

This script demonstrates how the Streamlit dashboard integrates with the 
overall Acoustic Guardian system.
"""

import streamlit as st
import time

def main():
    st.set_page_config(
        page_title="Acoustic Guardian - Streamlit Demo",
        page_icon="🌳",
        layout="centered"
    )
    
    st.title("Acoustic Guardian - Streamlit Integration")
    st.markdown("### Demonstrating the Power of Streamlit for Conservation Technology")
    
    # Introduction
    st.markdown("""
    The Acoustic Guardian system leverages Streamlit to provide:
    
    1. **Real-time Data Visualization** - Interactive maps and metrics
    2. **Sensor Monitoring** - Live status of all deployed devices
    3. **Threat Detection Timeline** - Historical view of all detections
    4. **Strategic Layer Integration** - Deforestation risk zones and protected areas
    5. **Mobile-Responsive Design** - Accessible on any device
    """)
    
    # System Architecture
    st.subheader("📊 System Architecture")
    st.markdown("""
    ```
    Hardware Sensors (ESP32 + Microphone)
                ↓
         Data Processing (Edge Impulse)
                ↓
        Communication (GSM/GPRS)
                ↓
         Cloud Storage (InfluxDB)
                ↓
      Streamlit Dashboard (Real-time Visualization)
                ↓
         Ranger Notification (SMS Alerts)
    ```
    """)
    
    # Key Features
    st.subheader("✨ Key Dashboard Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Real-time Map**")
        st.image("https://placehold.co/300x200?text=Interactive+Map", width=300)
        st.markdown("- Live sensor locations")
        st.markdown("- Threat hotspot visualization")
        st.markdown("- Strategic conservation layers")
        
        st.markdown("**System Metrics**")
        st.image("https://placehold.co/300x100?text=Metrics+Dashboard", width=300)
        st.markdown("- Detection counts")
        st.markdown("- Time safe tracking")
        st.markdown("- Device status monitoring")
    
    with col2:
        st.markdown("**Detection History**")
        st.image("https://placehold.co/300x150?text=Detection+Timeline", width=300)
        st.markdown("- Chronological view of threats")
        st.markdown("- Confidence levels")
        st.markdown("- Location tracking")
        
        st.markdown("**Strategic Insights**")
        st.image("https://placehold.co/300x150?text=Conservation+Layers", width=300)
        st.markdown("- Deforestation risk zones")
        st.markdown("- Protected area boundaries")
        st.markdown("- Reforestation projects")
    
    # Benefits of Streamlit
    st.subheader("🚀 Benefits of Using Streamlit")
    st.markdown("""
    - **Rapid Development**: Build interactive dashboards in minutes
    - **Python Native**: No web development skills required
    - **Real-time Updates**: Live data streaming capabilities
    - **Mobile Responsive**: Works on desktops, tablets, and phones
    - **Easy Deployment**: Simple hosting options available
    - **Open Source**: No licensing costs
    """)
    
    # Demo Controls
    st.subheader("🎮 Interactive Demo")
    
    if st.button("🚀 Launch Full Dashboard"):
        st.info("In a complete implementation, this would open the full Streamlit dashboard.")
        st.markdown("To run the dashboard locally:")
        st.code("""
        1. Install requirements: pip install -r requirements.txt
        2. Run the dashboard: streamlit run streamlit_dashboard.py
        3. Open browser to http://localhost:8501
        """, language="bash")
    
    # Simulation Controls
    st.subheader("🧪 Simulation Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 Simulate Detection"):
            st.success("Chainsaw detection simulated!")
            st.info("In the full dashboard, this would:")
            st.markdown("- Update the map with a red hotspot")
            st.markdown("- Reset the 'Time Safe' counter")
            st.markdown("- Add entry to detection history")
            st.markdown("- Potentially trigger SMS alerts")
    
    with col2:
        if st.button("💚 Send Heartbeat"):
            st.success("Device heartbeat sent!")
            st.info("In the full dashboard, this would:")
            st.markdown("- Update device status indicators")
            st.markdown("- Increment 'Time Safe' counter")
            st.markdown("- Log system health metrics")
    
    with col3:
        if st.button("🔄 Reset System"):
            st.success("System reset!")
            st.info("In the full dashboard, this would:")
            st.markdown("- Clear detection history")
            st.markdown("- Reset all counters")
            st.markdown("- Return to baseline state")
    
    # Footer
    st.markdown("---")
    st.markdown("🌳 Acoustic Guardian - Protecting forests with AI-powered acoustic monitoring")
    st.markdown("Built with Streamlit for rapid visualization and real-time insights")

if __name__ == "__main__":
    main()