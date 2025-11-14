#!/usr/bin/env python3
"""
Acoustic Guardian - Preview Simulation Script

This script demonstrates the core functionality of the Acoustic Guardian system
without requiring actual InfluxDB or Twilio accounts.
"""

import time
import random
from datetime import datetime

# Sensor configuration
DEVICE_ID = "AG-001"
SENSOR_LOCATION = "Amazon-Brazil"
RANGER_PHONE_NUMBER = "+1234567890"  # Demo number

# Fixed sensor location
SENSOR_LATITUDE = -3.4653
SENSOR_LONGITUDE = -62.2159

def simulate_influxdb_send(data):
    """
    Simulate sending data to InfluxDB
    """
    print(f"SIMULATED: Data sent to InfluxDB")
    print(f"  Data: {data}")
    return True

def simulate_sms_alert(message):
    """
    Simulate sending SMS alert
    """
    print(f"SIMULATED: SMS alert sent to {RANGER_PHONE_NUMBER}")
    print(f"  Message: {message}")
    return True

def simulate_chainsaw_detection():
    """
    Simulate a chainsaw detection event
    """
    print("\n" + "="*50)
    print("🚨 SIMULATING CHAINSAW DETECTION 🚨")
    print("="*50)
    
    # Generate high-confidence threat data
    threat_type = "chainsaw"
    confidence = round(random.uniform(0.90, 0.99), 2)  # 90-99% confidence
    gps_coordinates = f"{SENSOR_LATITUDE}, {SENSOR_LONGITUDE}"
    timestamp = int(time.time())
    
    print(f"Device ID: {DEVICE_ID}")
    print(f"Location: {SENSOR_LOCATION}")
    print(f"GPS Coordinates: {gps_coordinates}")
    print(f"Threat Type: {threat_type}")
    print(f"Confidence: {confidence*100:.1f}%")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create InfluxDB Line Protocol data
    line_protocol = (
        f"acoustic_guardian,device_id={DEVICE_ID},location={SENSOR_LOCATION} "
        f"gps_coordinates=\"{gps_coordinates}\",threat_type=\"{threat_type}\","
        f"confidence={confidence},threat_detected=true,time_safe=0 {timestamp}"
    )
    
    # Simulate sending data to InfluxDB
    if simulate_influxdb_send(line_protocol):
        # Simulate sending SMS alert
        sms_message = (
            f"🚨 ALERT! Chainsaw detected at {gps_coordinates} - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        simulate_sms_alert(sms_message)
        print("✅ Chainsaw detection simulation completed.")
        print("📊 Grafana dashboard would now show:")
        print("   - Red hotspot at sensor location")
        print("   - 'Time Safe' metric reset to 0")
        print("   - New threat entry in timeline")
    else:
        print("❌ Failed to simulate chainsaw detection.")

def simulate_heartbeat():
    """
    Simulate a safe heartbeat (periodic check)
    """
    print("\n" + "="*50)
    print("💚 SIMULATING SAFE HEARTBEAT 💚")
    print("="*50)
    
    # Generate heartbeat data
    battery_level = round(random.uniform(80.0, 100.0), 1)  # 80-100% battery
    signal_strength = random.randint(-80, -60)  # dBm
    timestamp = int(time.time())
    
    print(f"Device ID: {DEVICE_ID}")
    print(f"Battery Level: {battery_level}%")
    print(f"Signal Strength: {signal_strength} dBm")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create InfluxDB Line Protocol data for device status
    line_protocol = (
        f"device_status,device_id={DEVICE_ID} "
        f"battery_level={battery_level},signal_strength={signal_strength},"
        f"uptime={int(time.time())} {timestamp}"
    )
    
    # Simulate sending data to InfluxDB
    if simulate_influxdb_send(line_protocol):
        print("✅ Safe heartbeat simulation completed.")
        print("📊 Grafana dashboard would now show:")
        print("   - Updated device status")
        print("   - 'Time Safe' metric continuing to count up")
        print("   - Heartbeat entry in device timeline")
    else:
        print("❌ Failed to simulate safe heartbeat.")

def show_dashboard_preview():
    """
    Show what the Grafana dashboard would look like
    """
    print("\n" + "="*60)
    print("📊 GRAFANA DASHBOARD PREVIEW 📊")
    print("="*60)
    print()
    print("WORLD MAP PANEL:")
    print("  🟢 Sensor AG-001: Amazon-Brazil (-3.4653, -62.2159)")
    print("  📈 Time Safe: 127 minutes (since last threat)")
    print()
    print("THREAT TIMELINE:")
    print("  📅 Today at 10:32:15 - Chainsaw detected (95.2% confidence)")
    print("  📅 Today at 08:45:33 - Chainsaw detected (92.7% confidence)")
    print("  📅 Yesterday at 14:22:07 - Chainsaw detected (97.1% confidence)")
    print()
    print("DEVICE STATUS:")
    print("  🔋 Battery: 94%")
    print("  📶 Signal: -67 dBm")
    print("  ⏱️  Uptime: 2 days, 14:32:15")
    print()
    print("STRATEGIC LAYERS:")
    print("  🟠 Historical Deforestation Areas")
    print("  🔴 High-Risk Logging Zones")
    print("  🟣 Reforestation Projects")

def main():
    """
    Main simulation loop
    """
    print("Acoustic Guardian - Preview Simulation")
    print("=" * 40)
    print(f"Device ID: {DEVICE_ID}")
    print(f"Location: {SENSOR_LOCATION} ({SENSOR_LATITUDE}, {SENSOR_LONGITUDE})")
    print("=" * 40)
    
    # Show initial dashboard state
    show_dashboard_preview()
    
    # Simulation menu
    while True:
        print("\n" + "="*40)
        print("Select simulation action:")
        print("1. Simulate Chainsaw Detection (Threat Alert)")
        print("2. Simulate Safe Heartbeat")
        print("3. Show Dashboard Preview")
        print("4. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            simulate_chainsaw_detection()
        elif choice == "2":
            simulate_heartbeat()
        elif choice == "3":
            show_dashboard_preview()
        elif choice == "4":
            print("Exiting simulation.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()