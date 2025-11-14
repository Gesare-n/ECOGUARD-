#!/usr/bin/env python3
"""
Acoustic Guardian - Hardware Simulation Script

This script simulates the ESP32 hardware sensor by generating threat detection data
and sending it to InfluxDB and SMS alerts via Twilio, demonstrating the Digital Twin
functionality without requiring physical hardware.
"""

import requests
import time
import random
from datetime import datetime
import os
from twilio.rest import Client

# Sensor configuration
DEVICE_ID = "AG-001"
SENSOR_LOCATION = "Amazon-Brazil"
RANGER_PHONE_NUMBER = "+1234567890"  # Replace with actual ranger number

# InfluxDB configuration (update with your actual credentials)
INFLUXDB_URL = "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s"
INFLUXDB_TOKEN = "your-token-here"
INFLUXDB_ORG = "your-org"
INFLUXDB_BUCKET = "your-bucket"

# Twilio configuration (update with your actual credentials)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number

# Fixed sensor location (update with actual coordinates)
SENSOR_LATITUDE = -3.4653
SENSOR_LONGITUDE = -62.2159

def send_to_influxdb(data):
    """
    Send data to InfluxDB using the Line Protocol
    """
    headers = {
        "Authorization": f"Token {INFLUXDB_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    try:
        response = requests.post(INFLUXDB_URL, headers=headers, data=data)
        if response.status_code == 204:
            print(f"Data successfully sent to InfluxDB: {data}")
            return True
        else:
            print(f"Failed to send data to InfluxDB. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending data to InfluxDB: {str(e)}")
        return False

def send_sms_alert(message):
    """
    Send SMS alert via Twilio
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=RANGER_PHONE_NUMBER
        )
        print(f"SMS alert sent successfully. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False

def simulate_chainsaw_detection():
    """
    Simulate a chainsaw detection event
    """
    print("Simulating chainsaw detection...")
    
    # Generate high-confidence threat data
    threat_type = "chainsaw"
    confidence = round(random.uniform(0.90, 0.99), 2)  # 90-99% confidence
    gps_coordinates = f"{SENSOR_LATITUDE}, {SENSOR_LONGITUDE}"
    timestamp = int(time.time())
    
    # Create InfluxDB Line Protocol data
    line_protocol = (
        f"acoustic_guardian,device_id={DEVICE_ID},location={SENSOR_LOCATION} "
        f"gps_coordinates=\"{gps_coordinates}\",threat_type=\"{threat_type}\","
        f"confidence={confidence},threat_detected=true,time_safe=0 {timestamp}"
    )
    
    # Send data to InfluxDB
    if send_to_influxdb(line_protocol):
        # Send SMS alert
        sms_message = (
            f"ALERT! Chainsaw detected at {gps_coordinates} - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_sms_alert(sms_message)
        print("Chainsaw detection simulation completed.")
    else:
        print("Failed to simulate chainsaw detection.")

def simulate_heartbeat():
    """
    Simulate a safe heartbeat (periodic check)
    """
    print("Simulating safe heartbeat...")
    
    # Generate heartbeat data
    battery_level = round(random.uniform(80.0, 100.0), 1)  # 80-100% battery
    signal_strength = random.randint(-80, -60)  # dBm
    uptime = int(time.time() - start_time)
    timestamp = int(time.time())
    
    # Create InfluxDB Line Protocol data for device status
    line_protocol = (
        f"device_status,device_id={DEVICE_ID} "
        f"battery_level={battery_level},signal_strength={signal_strength},"
        f"uptime={uptime} {timestamp}"
    )
    
    # Send data to InfluxDB
    if send_to_influxdb(line_protocol):
        print("Safe heartbeat simulation completed.")
    else:
        print("Failed to simulate safe heartbeat.")

def main():
    """
    Main simulation loop
    """
    global start_time
    start_time = time.time()
    
    print("Acoustic Guardian - Hardware Simulation")
    print("=" * 40)
    print(f"Device ID: {DEVICE_ID}")
    print(f"Location: {SENSOR_LOCATION} ({SENSOR_LATITUDE}, {SENSOR_LONGITUDE})")
    print(f"Ranger Number: {RANGER_PHONE_NUMBER}")
    print("=" * 40)
    
    # Check if required environment variables are set
    missing_configs = []
    if INFLUXDB_URL == "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s":
        missing_configs.append("INFLUXDB_URL")
    if INFLUXDB_TOKEN == "your-token-here":
        missing_configs.append("INFLUXDB_TOKEN")
    if TWILIO_ACCOUNT_SID == "your_account_sid":
        missing_configs.append("TWILIO_ACCOUNT_SID")
    if TWILIO_AUTH_TOKEN == "your_auth_token":
        missing_configs.append("TWILIO_AUTH_TOKEN")
    if TWILIO_PHONE_NUMBER == "+1234567890":
        missing_configs.append("TWILIO_PHONE_NUMBER")
    if RANGER_PHONE_NUMBER == "+1234567890":
        missing_configs.append("RANGER_PHONE_NUMBER")
        
    if missing_configs:
        print("WARNING: The following configurations need to be updated:")
        for config in missing_configs:
            print(f"  - {config}")
        print("\nPlease update the configuration values in the script before running.")
        return
    
    # Simulation menu
    while True:
        print("\nSelect simulation action:")
        print("1. Simulate Chainsaw Detection (Threat Alert)")
        print("2. Simulate Safe Heartbeat")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            simulate_chainsaw_detection()
        elif choice == "2":
            simulate_heartbeat()
        elif choice == "3":
            print("Exiting simulation.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()