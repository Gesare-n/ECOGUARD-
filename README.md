# Acoustic Guardian MVP

An acoustic monitoring system for detecting chainsaw activity in protected forest areas using TinyML on the edge with SMS alerts and cloud data logging.

## Hardware Components

1. **TTGO T-Call ESP32 SIM800L** - Integrated GSM/MCU board
2. **INMP441 I2S Microphone** - High-quality digital microphone
3. **Antenna** for GSM connectivity

## System Architecture

```
[INMP441 Microphone] → [ESP32] → [Edge Impulse Model] → [Detection Logic]
                                    ↓
                        [SIM800L GSM Module] → SMS Alert
                                    ↓
                        [InfluxDB Cloud] → Data Logging
                                    ↓
            [Grafana Dashboard] ↔ [Streamlit Dashboard] → Visualization
```

## Features

1. **AI Detection**: Classifies chainsaw sounds with >90% confidence using Edge Impulse trained model
2. **Direct SMS Alert**: Sends immediate SMS to rangers upon detection with GPS coordinates
3. **Data Logging**: Transmits threat data to InfluxDB via GPRS
4. **Digital Twin Visualization**: Real-time dashboard with map hotspots and "Time Safe" metrics
5. **Strategic Layers**: Mocked-up deforestation and high-risk logging model layers
6. **Streamlit Dashboard**: Interactive Python-based visualization for real-time monitoring

## Setup Instructions

### Hardware Assembly (Physical Deployment)

1. Connect the INMP441 microphone to the ESP32:
   - INMP441 VDD → ESP32 3.3V
   - INMP441 GND → ESP32 GND
   - INMP441 L/R → ESP32 GND (for mono)
   - INMP441 WS → ESP32 GPIO 15
   - INMP441 SCK → ESP32 GPIO 2
   - INMP441 SD → ESP32 GPIO 13

2. The SIM800L is integrated on the TTGO T-Call board

### Software Setup (Physical Deployment)

1. Install required libraries in Arduino IDE:
   - TinyGPS++
   - WiFiClientSecure
   - HTTPClient

2. Configure the following in `main.ino`:
   - RANGER_PHONE_NUMBER
   - INFLUXDB_URL
   - INFLUXDB_TOKEN
   - APN settings for your mobile carrier

3. Upload the firmware to the ESP32

### Simulation Setup (Hackathon Demo)

For demonstration purposes without hardware, use the Python simulation script:

1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Update configuration values in `simulate_sensor.py`
3. Run the simulation:
   ```
   python simulate_sensor.py
   ```

### Edge Impulse Model Integration

1. Train your model on Edge Impulse Studio with chainsaw/nature sounds
2. Deploy the model as an ESP32 Arduino library
3. Replace the placeholder [detectChainsaw()](file:///D:/AcousticGuardian/main.ino#L99-L117) function with actual model inference code

### Cloud Services Setup

#### InfluxDB Cloud
1. Create a free account at influxdata.com
2. Create an organization and bucket
3. Generate an API token
4. Update the credentials in the firmware

#### Grafana Dashboard
1. Sign up for Grafana Cloud or install locally
2. Add InfluxDB as a data source
3. Import the provided dashboard template
4. Configure Worldmap panel with appropriate coordinates

#### Streamlit Dashboard
1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
2. Run the Streamlit dashboard:
   ```
   streamlit run streamlit_dashboard.py
   ```
3. Access the dashboard at http://localhost:8501
4. For Windows users, simply run `run_dashboard.bat`

#### Nairobi Forest Dashboard
1. Install required Python packages (if not already installed):
   ```
   pip install -r requirements.txt
   ```
2. Run the Nairobi dashboard:
   ```
   streamlit run nairobi_dashboard.py
   ```
3. Access the dashboard at http://localhost:8504
4. For Windows users, simply run `run_nairobi_dashboard.bat`

#### Deforestation Analysis Dashboard
1. Install required Python packages (if not already installed):
   ```
   pip install -r requirements.txt
   ```
2. Run the deforestation analysis dashboard:
   ```
   streamlit run deforestation_analysis.py
   ```
3. Access the dashboard at http://localhost:8505
4. For Windows users, simply run `run_deforestation_analysis.bat`

#### Institutional Dashboard
1. Install required Python packages (if not already installed):
   ```
   pip install -r requirements.txt
   ```
2. Run the institutional dashboard:
   ```
   streamlit run institutional_dashboard.py
   ```
3. Access the dashboard at http://localhost:8506
4. For Windows users, simply run `run_institutional_dashboard.bat`

#### Research Dashboard
1. Install required Python packages (if not already installed):
   ```
   pip install -r requirements.txt
   ```
2. Run the research dashboard:
   ```
   streamlit run research_dashboard.py
   ```
3. Access the dashboard at http://localhost:8507
4. For Windows users, simply run `run_research_dashboard.bat`

#### Policy & Carbon Credit Dashboard
1. Install required Python packages (if not already installed):
   ```
   pip install -r requirements.txt
   ```
2. Run the policy dashboard:
   ```
   streamlit run policy_dashboard.py
   ```
3. Access the dashboard at http://localhost:8508
4. For Windows users, simply run `run_policy_dashboard.bat`

## Versatility

The core technology can be adapted for other conservation challenges:

| Problem | Required Model Retraining |
|---------|---------------------------|
| Poaching | Gunshots, Vehicle Engines |
| Illegal Fishing | Boat Engines |
| Wildlife Monitoring | Specific Animal Calls |

## Testing

To test the system:
1. Upload firmware to ESP32
2. Place in test environment
3. Play chainsaw audio sample near microphone
4. Verify SMS receipt
5. Check InfluxDB for data
6. Confirm Grafana dashboard updates

## Troubleshooting

- Ensure SIM card has active service and sufficient credit
- Check antenna connection for GSM module
- Verify InfluxDB credentials and network connectivity
- Confirm GPS has clear sky view for coordinate acquisition