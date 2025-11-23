# Acoustic Guardian - Digital Hummingbird Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Digital Hummingbird sensor node in a forest environment. The deployment process includes hardware assembly, software installation, configuration, and testing.

## Prerequisites
1. All components from the Bill of Materials
2. Raspberry Pi Imager or similar tool
3. Computer with internet access
4. MicroSD card reader
5. Basic soldering equipment
6. 3D printer (or access to printed enclosure)

## Hardware Assembly

### 1. Prepare the Raspberry Pi
1. Install the Raspberry Pi OS on the MicroSD card using Raspberry Pi Imager
2. Insert the MicroSD card into the Raspberry Pi
3. Connect the Pi Camera Module to the CSI port
4. Connect the USB microphone to one of the USB ports

### 2. Connect Communication Modules
1. Connect the LoRa module to the Raspberry Pi GPIO pins:
   - VCC → 3.3V (Pin 1)
   - GND → Ground (Pin 6)
   - SCK → GPIO 11 (Pin 23)
   - MISO → GPIO 9 (Pin 21)
   - MOSI → GPIO 10 (Pin 19)
   - NSS → GPIO 18 (Pin 12)
   - RST → GPIO 14 (Pin 8)
   - DIO0 → GPIO 26 (Pin 37)

2. Connect the GSM module:
   - Connect via USB or UART pins
   - Ensure the antenna is properly attached

### 3. Connect Sensors
1. Connect the GPS module to the UART pins or USB
2. Connect the DHT22 sensor:
   - VCC → 3.3V
   - GND → Ground
   - Data → GPIO 4

### 4. Assemble Power System
1. Connect the solar panel to the battery charging module
2. Connect the battery to the power management board
3. Connect the power management board output to the Raspberry Pi

### 5. Install in Enclosure
1. Place all components in the 3D-printed bird-shaped enclosure
2. Ensure all connections are secure and weatherproof
3. Seal the enclosure with appropriate gaskets

## Software Installation

### 1. Initial Raspberry Pi Setup
1. Boot the Raspberry Pi and complete initial setup
2. Connect to Wi-Fi or Ethernet for internet access
3. Enable camera interface: `sudo raspi-config` → Interfacing Options → Camera → Enable
4. Enable I2C: `sudo raspi-config` → Interfacing Options → I2C → Enable

### 2. Install Required Software
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
pip3 install -r requirements.txt

# Install additional system packages
sudo apt install git python3-opencv libatlas-base-dev -y
```

### 3. Configure the System
1. Clone the Acoustic Guardian repository:
   ```bash
   git clone https://github.com/yourusername/acoustic-guardian.git
   cd acoustic-guardian
   ```

2. Update the configuration file `rpi_config.py` with your specific settings:
   - Device ID and name
   - Ranger phone number
   - InfluxDB credentials
   - LoRa settings
   - GSM APN settings

3. Set up environment variables for Twilio:
   ```bash
   export TWILIO_ACCOUNT_SID="your_account_sid"
   export TWILIO_AUTH_TOKEN="your_auth_token"
   ```

### 4. Install AI Models
1. Download or train your acoustic detection model
2. Convert to TensorFlow Lite format
3. Place in the `models/` directory
4. Update paths in `rpi_config.py`

### 5. Set Up Auto-start
1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/acoustic-guardian.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Acoustic Guardian Digital Hummingbird
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/acoustic-guardian
   ExecStart=/usr/bin/python3 /home/pi/acoustic-guardian/rpi_main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable acoustic-guardian.service
   sudo systemctl start acoustic-guardian.service
   ```

## Testing and Validation

### 1. Hardware Testing
1. Verify all connections with a multimeter
2. Test each sensor individually:
   - GPS: Check for satellite lock
   - Camera: Capture test image
   - Microphone: Record test audio
   - LoRa: Test communication range
   - GSM: Verify network connection

### 2. Software Testing
1. Run the main script manually to check for errors:
   ```bash
   python3 rpi_main.py
   ```

2. Verify data transmission:
   - Check LoRa gateway for received packets
   - Verify InfluxDB for data points
   - Test SMS alert functionality

3. Monitor system logs:
   ```bash
   tail -f acoustic_guardian.log
   ```

### 3. Field Testing
1. Deploy a single unit in a controlled environment
2. Monitor performance for 24-48 hours
3. Check battery consumption and solar charging
4. Verify all communication methods
5. Validate detection accuracy

## Deployment in Forest Environment

### 1. Site Selection
1. Choose locations based on:
   - High-risk logging areas
   - Reforestation zones
   - Areas with adequate sunlight for solar charging
   - Clear line of sight for LoRa communication

### 2. Installation
1. Mount the Digital Hummingbird securely:
   - Use appropriate mounting hardware
   - Ensure the enclosure is level
   - Position camera for optimal tree monitoring
   - Orient antennas for best signal reception

2. Secure all cables and connections
3. Test communication with gateway
4. Register the device in the central system

### 3. Network Configuration
1. Configure LoRa gateway:
   - Set appropriate frequency and spreading factor
   - Connect to internet for data forwarding
   - Configure data routing to InfluxDB

2. Verify data flow:
   - Check that data appears in InfluxDB
   - Verify dashboard visualization
   - Confirm alert system functionality

## Maintenance and Monitoring

### 1. Regular Maintenance
1. Monthly:
   - Check battery levels
   - Clean solar panels
   - Inspect enclosure for damage
   - Verify all connections

2. Quarterly:
   - Update software and models
   - Calibrate sensors if needed
   - Check mounting hardware

### 2. Remote Monitoring
1. Monitor system health through:
   - Dashboard metrics
   - Automated alerts
   - Periodic status reports

2. Troubleshooting:
   - Check logs for errors
   - Verify power and communication
   - Remote restart if necessary

## Troubleshooting Common Issues

### 1. No Data Transmission
- Check LoRa antenna connection
- Verify gateway is online
- Check InfluxDB credentials
- Review network connectivity

### 2. False Detections
- Review acoustic model accuracy
- Check microphone placement
- Adjust detection threshold
- Update model with new training data

### 3. Power Issues
- Check solar panel orientation
- Verify battery connections
- Monitor power consumption
- Check for component failures

### 4. Communication Failures
- Verify GSM signal strength
- Check SIM card activation
- Review APN settings
- Test with different carrier

## Scaling the Network

### 1. Adding More Nodes
1. Follow the same deployment process for each new node
2. Assign unique device IDs
3. Register in the central system
4. Configure dashboard for new locations

### 2. Expanding LoRa Coverage
1. Add additional gateways for larger areas
2. Configure gateway clustering
3. Optimize frequency planning
4. Monitor network performance

### 3. Data Management
1. Implement data archiving policies
2. Set up backup systems
3. Monitor database performance
4. Plan for capacity growth

## Conclusion
The Digital Hummingbird provides a comprehensive solution for forest monitoring with its unique combination of acoustic detection, visual monitoring, and robust communication. Following this deployment guide will ensure successful implementation and long-term operation in forest environments.