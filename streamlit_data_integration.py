"""
Acoustic Guardian - Streamlit Data Integration

This script demonstrates how the Streamlit dashboard would integrate with 
real data sources like InfluxDB in a production environment.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random

# Mock data generator to simulate InfluxDB data
def generate_mock_data(hours=24, sensors=1):
    """
    Generate mock sensor data for demonstration
    """
    data = []
    now = datetime.now()
    
    for i in range(sensors):
        sensor_id = f"AG-{str(i+1).zfill(3)}"
        base_lat = -3.4653 + random.uniform(-0.1, 0.1)
        base_lng = -62.2159 + random.uniform(-0.1, 0.1)
        
        # Generate baseline readings
        for h in range(hours):
            timestamp = now - timedelta(hours=h)
            
            # Occasionally generate detections
            if random.random() < 0.1:  # 10% chance of detection
                detection = {
                    'timestamp': timestamp,
                    'sensor_id': sensor_id,
                    'latitude': base_lat + random.uniform(-0.01, 0.01),
                    'longitude': base_lng + random.uniform(-0.01, 0.01),
                    'threat_type': 'Chainsaw',
                    'confidence': round(random.uniform(90, 99), 1),
                    'battery_level': round(random.uniform(80, 100), 1),
                    'signal_strength': random.randint(-80, -60),
                    'event_type': 'detection'
                }
                data.append(detection)
            
            # Generate heartbeat data
            heartbeat = {
                'timestamp': timestamp,
                'sensor_id': sensor_id,
                'latitude': base_lat,
                'longitude': base_lng,
                'threat_type': None,
                'confidence': None,
                'battery_level': round(random.uniform(80, 100), 1),
                'signal_strength': random.randint(-80, -60),
                'event_type': 'heartbeat'
            }
            data.append(heartbeat)
    
    return pd.DataFrame(data)

# Function to simulate InfluxDB query
def query_influxdb_mock(query):
    """
    Mock function to simulate querying InfluxDB
    In a real implementation, this would connect to InfluxDB and execute the query
    """
    if 'last_detection' in query:
        # Return mock last detection
        return pd.DataFrame([{
            'sensor_id': 'AG-001',
            'timestamp': datetime.now() - timedelta(minutes=30),
            'latitude': -3.4653,
            'longitude': -62.2159,
            'threat_type': 'Chainsaw',
            'confidence': 95.2
        }])
    elif 'detection_history' in query:
        # Return mock detection history
        return generate_mock_data(hours=168, sensors=3)  # Last 7 days, 3 sensors
    elif 'sensor_status' in query:
        # Return mock sensor status
        return pd.DataFrame([{
            'sensor_id': 'AG-001',
            'battery_level': 94.5,
            'signal_strength': -67,
            'last_seen': datetime.now() - timedelta(minutes=5)
        }])
    else:
        return pd.DataFrame()

# Streamlit app
def main():
    st.set_page_config(
        page_title="Acoustic Guardian - Data Integration Demo",
        page_icon="🌳",
        layout="wide"
    )
    
    st.title("Acoustic Guardian - Data Integration Demo")
    st.markdown("### Demonstrating Integration with InfluxDB Time-Series Data")
    
    # Introduction
    st.markdown("""
    This demo shows how the Streamlit dashboard would integrate with real data sources:
    
    1. **InfluxDB Integration** - Querying time-series data
    2. **Real-time Updates** - Streaming new detections
    3. **Data Processing** - Converting raw data to insights
    4. **Performance Optimization** - Efficient data handling
    """)
    
    # Data Integration Demo
    st.subheader("🔌 Data Integration Example")
    
    # Simulate querying different data sources
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Last Detection Query**")
        last_detection_query = """
        from(bucket: "acoustic-guardian")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "acoustic_guardian" and r.threat_detected == true)
          |> last()
        """
        st.code(last_detection_query, language="flux")
        
        if st.button("Execute Last Detection Query"):
            with st.spinner("Querying InfluxDB..."):
                time.sleep(1)  # Simulate network delay
                result = query_influxdb_mock("last_detection")
                st.success("Query executed successfully!")
                st.dataframe(result)
    
    with col2:
        st.markdown("**Sensor Status Query**")
        sensor_status_query = """
        from(bucket: "acoustic-guardian")
          |> range(start: -10m)
          |> filter(fn: (r) => r._measurement == "device_status")
          |> last()
        """
        st.code(sensor_status_query, language="flux")
        
        if st.button("Execute Sensor Status Query"):
            with st.spinner("Querying InfluxDB..."):
                time.sleep(1)  # Simulate network delay
                result = query_influxdb_mock("sensor_status")
                st.success("Query executed successfully!")
                st.dataframe(result)
    
    # Real-time Data Streaming
    st.subheader("🔄 Real-time Data Streaming")
    st.markdown("""
    The dashboard would continuously stream new data from InfluxDB:
    
    - New detections appear immediately on the map
    - Metrics update in real-time
    - Alerts trigger automatically
    """)
    
    # Simulate real-time data
    if st.button("Start Real-time Simulation"):
        placeholder = st.empty()
        
        for i in range(10):
            with placeholder.container():
                # Generate new mock data point
                new_data = {
                    'timestamp': datetime.now(),
                    'sensor_id': 'AG-001',
                    'latitude': -3.4653 + random.uniform(-0.001, 0.001),
                    'longitude': -62.2159 + random.uniform(-0.001, 0.001),
                    'battery_level': round(random.uniform(90, 100), 1),
                    'signal_strength': random.randint(-70, -60)
                }
                
                st.info(f"📡 New data point received: {new_data['timestamp'].strftime('%H:%M:%S')}")
                st.json(new_data)
                
                time.sleep(1)  # Wait 1 second between updates
        
        st.success("Real-time simulation complete!")
    
    # Data Processing Pipeline
    st.subheader("⚙️ Data Processing Pipeline")
    st.markdown("""
    Raw sensor data is processed to extract meaningful insights:
    
    1. **Data Cleaning** - Remove invalid readings
    2. **Geospatial Analysis** - Cluster detections
    3. **Temporal Analysis** - Identify patterns
    4. **Alert Generation** - Trigger notifications
    """)
    
    # Show data processing example
    if st.button("Show Data Processing Example"):
        # Generate raw data
        raw_data = generate_mock_data(hours=24, sensors=1)
        
        st.markdown("**Raw Sensor Data**")
        st.dataframe(raw_data.head(10))
        
        # Process data
        st.markdown("**Processed Insights**")
        
        # Detection summary
        detections = raw_data[raw_data['event_type'] == 'detection']
        if not detections.empty:
            st.metric(
                label="Total Detections (24h)", 
                value=len(detections),
                delta=f"{len(detections)} new"
            )
            
            avg_confidence = detections['confidence'].mean()
            st.metric(
                label="Average Confidence", 
                value=f"{avg_confidence:.1f}%",
                delta="High accuracy"
            )
        
        # Battery status
        latest_status = raw_data[raw_data['event_type'] == 'heartbeat'].iloc[-1]
        st.metric(
            label="Battery Level", 
            value=f"{latest_status['battery_level']:.1f}%",
            delta="Healthy"
        )
    
    # Performance Considerations
    st.subheader("⚡ Performance Considerations")
    st.markdown("""
    For production deployments:
    
    - **Caching** - Store frequently accessed data
    - **Pagination** - Limit data transfer
    - **Connection Pooling** - Reuse database connections
    - **Asynchronous Queries** - Non-blocking data fetching
    - **Data Archiving** - Move old data to cold storage
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("🌳 Acoustic Guardian - Data Integration Demo")

if __name__ == "__main__":
    main()