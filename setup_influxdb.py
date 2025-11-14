#!/usr/bin/env python3
"""
Utility script to help set up InfluxDB for Acoustic Guardian
"""

def print_influxdb_setup_instructions():
    """
    Print instructions for setting up InfluxDB
    """
    print("InfluxDB Setup Instructions")
    print("=" * 25)
    print()
    print("1. Sign up for a free InfluxDB Cloud account at https://cloud.influxdata.com/")
    print("2. Create a new organization (or use the default)")
    print("3. Create a new bucket named 'acoustic-guardian'")
    print("4. Generate an API token with read/write permissions to the bucket")
    print("5. Note the following information for configuration:")
    print("   - Organization name")
    print("   - Bucket name ('acoustic-guardian')")
    print("   - API token")
    print("   - InfluxDB URL (shown in the UI after setup)")
    print()
    print("Configuration Required in simulate_sensor.py:")
    print("- INFLUXDB_URL: Your InfluxDB write endpoint")
    print("- INFLUXDB_TOKEN: Your API token")
    print("- INFLUXDB_ORG: Your organization name")
    print("- INFLUXDB_BUCKET: 'acoustic-guardian'")

def show_sample_data_structure():
    """
    Show the expected data structure for InfluxDB
    """
    print("\nExpected Data Structure")
    print("=" * 23)
    print()
    print("Measurement: acoustic_guardian")
    print("Tags:")
    print("  - device_id (string): Unique identifier for the device")
    print("  - location (string): General location name")
    print("Fields:")
    print("  - gps_coordinates (string): Latitude and longitude")
    print("  - threat_type (string): Type of threat detected")
    print("  - confidence (float): Confidence level (0.0-1.0)")
    print("  - threat_detected (boolean): Whether threat was detected")
    print("  - time_safe (integer): Seconds since last threat")
    print()
    print("Sample Line Protocol:")
    print('acoustic_guardian,device_id=AG-001,location=Amazon-Brazil gps_coordinates="-3.4653, -62.2159",threat_type="chainsaw",confidence=0.95,threat_detected=true,time_safe=0 1634567890')

if __name__ == "__main__":
    print("Acoustic Guardian - InfluxDB Setup Helper")
    print()
    print_influxdb_setup_instructions()
    show_sample_data_structure()