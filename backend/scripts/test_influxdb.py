#!/usr/bin/env python3
"""
Test script for InfluxDB connectivity
"""

import requests
import time
import os

# InfluxDB configuration (update with your actual credentials)
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "your-token-here")

def test_influxdb_connection():
    """
    Test connection to InfluxDB
    """
    headers = {
        "Authorization": f"Token {INFLUXDB_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    # Simple test data
    test_data = "test_measurement,device_id=test-001 value=42"
    
    try:
        response = requests.post(INFLUXDB_URL, headers=headers, data=test_data)
        if response.status_code == 204:
            print("SUCCESS: Connected to InfluxDB and wrote test data")
            return True
        else:
            print(f"FAILED: InfluxDB returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: Failed to connect to InfluxDB: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing InfluxDB connection...")
    test_influxdb_connection()