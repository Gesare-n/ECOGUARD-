#!/usr/bin/env python3
"""
Utility script to help set up the Grafana dashboard for Acoustic Guardian
"""

import json
import requests

def print_dashboard_setup_instructions():
    """
    Print instructions for setting up the Grafana dashboard
    """
    print("Grafana Dashboard Setup Instructions")
    print("=" * 35)
    print()
    print("1. Log into your Grafana instance")
    print("2. Click the '+' icon on the left sidebar and select 'Import'")
    print("3. Upload the grafana_dashboard.json file or paste its contents")
    print("4. Select your InfluxDB data source when prompted")
    print("5. Click 'Import' to create the dashboard")
    print()
    print("Configuration Required:")
    print("- Ensure your InfluxDB data source is properly configured in Grafana")
    print("- Verify the bucket name matches 'acoustic-guardian'")
    print("- Confirm the measurement names match those in influxdb_schema.md")

def validate_dashboard_json():
    """
    Validate that the Grafana dashboard JSON file is properly formatted
    """
    try:
        with open('grafana_dashboard.json', 'r') as f:
            dashboard_data = json.load(f)
        
        # Check if this looks like a valid Grafana dashboard
        if 'dashboard' in dashboard_data and 'panels' in dashboard_data['dashboard']:
            print("✓ grafana_dashboard.json appears to be valid")
            print(f"  Dashboard title: {dashboard_data['dashboard'].get('title', 'Unknown')}")
            print(f"  Number of panels: {len(dashboard_data['dashboard']['panels'])}")
            return True
        else:
            print("✗ grafana_dashboard.json may not be a valid Grafana dashboard")
            return False
    except Exception as e:
        print(f"✗ Error reading grafana_dashboard.json: {str(e)}")
        return False

if __name__ == "__main__":
    print("Acoustic Guardian - Grafana Setup Helper")
    print()
    
    # Validate the dashboard JSON
    validate_dashboard_json()
    
    print()
    print_dashboard_setup_instructions()