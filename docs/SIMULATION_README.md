# Acoustic Guardian - Hardware Simulation

This simulation allows you to demonstrate the complete Acoustic Guardian system without requiring physical hardware. The Python script acts as a "Proxy Sensor" that simulates the functions of the ESP32 hardware.

## Prerequisites

1. Python 3.6 or higher
2. InfluxDB Cloud account
3. Twilio account (for SMS alerts)

## Setup Instructions

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Update the configuration values in [simulate_sensor.py](file:///D:/AcousticGuardian/simulate_sensor.py):
   - `INFLUXDB_URL`: Your InfluxDB write endpoint
   - `INFLUXDB_TOKEN`: Your InfluxDB API token
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `TWILIO_PHONE_NUMBER`: Your Twilio phone number
   - `RANGER_PHONE_NUMBER`: The phone number to receive alerts

## Running the Simulation

Execute the simulation script:
```
python simulate_sensor.py
```

The script will present a menu with options to simulate different sensor events.

## Demonstration Flow

1. **Initial State**: Grafana Dashboard shows all sensors Green and the "Time Safe" metric counting up.

2. **Trigger Threat**: Select option 1 to simulate a "Chainsaw" alert.
   - The script sends threat data to InfluxDB
   - An SMS alert is sent via Twilio

3. **Real-Time Update**: Within 2-5 seconds, the Grafana map shows a Red Hotspot at the sensor's location, and the "Time Safe" metric resets to zero.

4. **Trigger Heartbeat**: Select option 2 to simulate a "Safe Heartbeat".
   - The script sends device status data to InfluxDB
   - The Grafana dashboard logs the new heartbeat
   - The "Time Safe" metric begins counting up again.

## Troubleshooting

- Ensure all configuration values are correctly set
- Verify network connectivity to InfluxDB and Twilio
- Check that your InfluxDB bucket and organization are correctly configured
- Confirm that your Twilio account has sufficient credits and the phone number is correctly configured