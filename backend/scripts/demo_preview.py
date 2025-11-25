#!/usr/bin/env python3
"""
EcoGuard - Automated Demo Preview

This script automatically demonstrates the key features of the EcoGuard system.
"""

import time
import random
from datetime import datetime

def demo_chainsaw_detection():
    """
    Demonstrate chainsaw detection
    """
    print("\n" + "="*60)
    print("🚨 DEMONSTRATION: CHAINSAW DETECTION 🚨")
    print("="*60)
    
    # Generate detection data
    device_id = "AG-001"
    location = "Amazon-Brazil"
    lat, lng = -3.4653, -62.2159
    threat_type = "chainsaw"
    confidence = 95.2
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Device ID: {device_id}")
    print(f"Location: {location} ({lat}, {lng})")
    print(f"Threat Type: {threat_type}")
    print(f"Confidence: {confidence}%")
    print(f"Timestamp: {timestamp}")
    
    print("\n📡 SENDING DATA...")
    time.sleep(1)
    print("✅ Data sent to InfluxDB")
    time.sleep(0.5)
    print("✅ SMS alert sent to ranger")
    
    print("\n📊 DASHBOARD UPDATE:")
    print("   🔴 Red hotspot appearing on map...")
    time.sleep(1)
    print("   📉 'Time Safe' metric resetting to 0...")
    time.sleep(1)
    print("   📝 New entry in threat timeline...")
    
    print("\n✅ CHAINSAW DETECTION COMPLETE")

def demo_safe_heartbeat():
    """
    Demonstrate safe heartbeat
    """
    print("\n" + "="*60)
    print("💚 DEMONSTRATION: SAFE HEARTBEAT 💚")
    print("="*60)
    
    # Generate heartbeat data
    device_id = "AG-001"
    battery = 94
    signal = -67
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Device ID: {device_id}")
    print(f"Battery Level: {battery}%")
    print(f"Signal Strength: {signal} dBm")
    print(f"Timestamp: {timestamp}")
    
    print("\n📡 SENDING DATA...")
    time.sleep(1)
    print("✅ Status data sent to InfluxDB")
    
    print("\n📊 DASHBOARD UPDATE:")
    print("   🟢 Device status updated...")
    time.sleep(1)
    print("   📈 'Time Safe' metric continuing to count...")
    time.sleep(1)
    print("   📝 New heartbeat entry logged...")
    
    print("\n✅ SAFE HEARTBEAT COMPLETE")

def demo_dashboard_overview():
    """
    Show dashboard overview
    """
    print("\n" + "="*60)
    print("📊 DASHBOARD OVERVIEW 📊")
    print("="*60)
    
    print("WORLD MAP PANEL:")
    print("  🟢 Sensor AG-001: Amazon-Brazil (-3.4653, -62.2159)")
    print("  📈 Time Safe: 127 minutes (since last threat)")
    
    print("\nTHREAT TIMELINE:")
    print("  📅 Today at 10:32:15 - Chainsaw detected (95.2% confidence)")
    print("  📅 Today at 08:45:33 - Chainsaw detected (92.7% confidence)")
    print("  📅 Yesterday at 14:22:07 - Chainsaw detected (97.1% confidence)")
    
    print("\nDEVICE STATUS:")
    print("  🔋 Battery: 94%")
    print("  📶 Signal: -67 dBm")
    print("  ⏱️  Uptime: 2 days, 14:32:15")
    
    print("\nSTRATEGIC LAYERS:")
    print("  🟠 Historical Deforestation Areas")
    print("  🔴 High-Risk Logging Zones")
    print("  🟣 Reforestation Projects")

def main():
    """
    Run the automated demo
    """
    print("ACOUSTIC GUARDIAN - SYSTEM PREVIEW")
    print("="*50)
    print("Demonstrating the core capabilities of the system")
    print()
    
    # Show dashboard overview
    demo_dashboard_overview()
    time.sleep(3)
    
    # Demonstrate chainsaw detection
    demo_chainsaw_detection()
    time.sleep(3)
    
    # Demonstrate safe heartbeat
    demo_safe_heartbeat()
    time.sleep(2)
    
    print("\n" + "="*60)
    print("🎉 DEMONSTRATION COMPLETE 🎉")
    print("="*60)
    print("The EcoGuard system provides:")
    print("  • Real-time chainsaw detection with >90% accuracy")
    print("  • Instant SMS alerts to rangers")
    print("  • Live dashboard visualization")
    print("  • Strategic conservation insights")
    print("\nThis simulation demonstrates the system without")
    print("requiring physical hardware or cloud services.")

if __name__ == "__main__":
    main()