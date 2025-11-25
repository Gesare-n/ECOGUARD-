# EcoGuard - Digital Hummingbird

An acoustic monitoring system for detecting chainsaw activity in protected forest areas using AI on the edge with Telegram alerts and cloud data logging. Enhanced with Raspberry Pi, LoRa communication, and visual tree health monitoring in a bird-shaped enclosure.

## Hardware Components

### Raspberry Pi "Digital Hummingbird" Implementation
1. **Raspberry Pi 4 Model B** - Main processing unit
2. **USB Microphone** - Audio capture for acoustic detection
3. **Pi Camera Module v2** - Visual tree health monitoring
4. **LoRa Module (SX1278)** - Long-range radio communication
5. **SIM800L GSM Module** - SMS alerts and GPRS backup
6. **Solar Power System** - Renewable energy source
7. **Transparent Bird-shaped Enclosure** - 3D printed PLA housing

## System Architecture

### Raspberry Pi "Digital Hummingbird" Architecture
EcoGuard
[USB Microphone] → [Raspberry Pi] → [TensorFlow Lite Model] → [Acoustic Detection]
[Pi Camera] → [Raspberry Pi] → [TensorFlow Lite Model] → [Tree Health Monitoring]
                                   ↓
                       [LoRa Module] → [LoRa Gateway] → [InfluxDB Cloud]
                                   ↓
                       [Telegram Bot] → Alert Notification
                                   ↓
           [Grafana Dashboard] ↔ [Streamlit Dashboard] → Visualization
EcoGuard

## Features

1. **AI Detection**: Classifies chainsaw sounds with >90% confidence using TensorFlow Lite models
2. **Telegram Alert**: Sends immediate alerts to rangers via Telegram bot upon detection with GPS coordinates
3. **Data Logging**: Transmits threat data to InfluxDB via LoRa and GPRS backup
4. **Digital Twin Visualization**: Real-time dashboard with map hotspots and "Time Safe" metrics
5. **Strategic Layers**: Mocked-up deforestation and high-risk logging model layers
6. **Streamlit Dashboard**: Interactive Python-based visualization for real-time monitoring
7. **Kenya Forest Data Integration**: Enhanced visualization with real Kenyan forest boundaries and risk assessment
8. **Tree Survival Rate Tracking**: Visual AI tracks planted sapling health and survival rates
9. **LoRa Hybrid Communication**: Redundant data transmission with LoRa for bulk data and GSM for critical alerts
10. **Bird-shaped Enclosure**: Transparent, aesthetically pleasing design that aligns with the "Hummingbird" narrative

## Enhanced Authentication System

The EcoGuard system now includes a role-based authentication system with three user types:

1. **Forest Ranger** - Basic monitoring access for field personnel
2. **Regional Manager** - Extended access with reporting capabilities
3. **Super User** - Full system access including user management

### Default Credentials

- Forest Ranger: username `ranger1`, password `password`
- Regional Manager: username `manager1`, password `password`
- Super User: username `admin`, password `password`

### Running the Enhanced System

To run the enhanced dashboard with authentication:

```bash
# Using the batch file (Windows)
run_enhanced_dashboard.bat

# Or directly with Streamlit
streamlit run app.py
```

The system will automatically redirect unauthenticated users to the login page.

## Unified Access Point

All EcoGuard services can be accessed from a single localhost entry point:

- **Modern React Frontend**: http://localhost:8080
- **API Server**: http://localhost:5000
- **Streamlit Dashboards**: Various ports (8501-8507)

### Starting All Services

1. Start the API server:
   ```bash
   python api_endpoints.py
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npx vite --port 8080
   ```

3. Start all Streamlit dashboards:
   ```bash
   run_all_dashboards.bat
   ```

### Accessing Services

Once all services are running:

1. **Modern Interface**: Visit http://localhost:8080 to access the new React frontend
   - Log in with any of the default credentials
   - Navigate to "Legacy Dashboards" to access Streamlit dashboards

2. **Direct Dashboard Access**:
   - Main Dashboard: http://localhost:8501
   - Institutional Dashboard: http://localhost:8502
   - Policy Dashboard: http://localhost:8503
   - Research Dashboard: http://localhost:8504
   - Nairobi Dashboard: http://localhost:8505
   - Enhanced Dashboard: http://localhost:8506
   - Super User Dashboard: http://localhost:8507

### Troubleshooting Proxy Issues

If you're experiencing issues with the proxy not working correctly:

1. **Check Vite Configuration**: Ensure `vite.config.ts` is in the `frontend` directory with the correct proxy settings:
   ```typescript
   export default defineConfig({
     server: {
       host: "localhost",
       port: 8080,
       proxy: {
         '/api': {
           target: 'http://localhost:5000',
           changeOrigin: true,
           secure: false,
         }
       }
     }
   });
   ```

2. **Restart Services**: Stop all running services and restart them in order:
   - API server (port 5000)
   - Frontend development server (port 8080)

3. **Test API Directly**: Verify the API server is working by accessing http://localhost:5000/api/auth/login directly

4. **Check Network**: Ensure no firewall is blocking the connections between services

## Setup Instructions

### Hardware Assembly (Physical Deployment)

#### Raspberry Pi "Digital Hummingbird" Implementation
1. Follow the detailed instructions in `rpi_deployment_guide.md`
2. Assemble components according to the pin connections specified
3. Install in the 3D-printed bird-shaped enclosure

### Software Setup (Physical Deployment)

#### Raspberry Pi "Digital Hummingbird" Implementation
1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Update configuration values in `rpi_config.py`
3. Set up environment variables for Twilio:
   ```bash
   export TWILIO_ACCOUNT_SID="your_account_sid"
   export TWILIO_AUTH_TOKEN="your_auth_token"
   ```

4. Run the main script:
   ```bash
   python rpi_main.py
   ```

### Simulation Setup (Hackathon Demo)

For demonstration purposes without hardware, use the Python simulation script:

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Update configuration values in `simulate_sensor.py`
3. Run the simulation:
   ```bash
   python simulate_sensor.py
   ```

### Kenya Forest Data Integration

Enhance the Digital Twin with real Kenyan forest data:

1. Install additional requirements:
   ```bash
   pip install geopandas
   ```

2. Run the data integration script:
   ```bash
   python kenya_forest_data_integration.py
   ```

3. Follow the guide in `kenya_data_integration_guide.md` for full implementation

### AI Model Integration

#### Raspberry Pi "Digital Hummingbird" Implementation
1. Train acoustic detection model with TensorFlow
2. Convert to TensorFlow Lite format
3. Place in the `models/` directory
4. Update paths in `rpi_config.py`

### Cloud Services Setup

#### InfluxDB Cloud
1. Create a free account at influxdata.com
2. Create an organization and bucket
3. Generate an API token
4. Update the credentials in the configuration files

#### Grafana Dashboard
1. Sign up for Grafana Cloud or install locally
2. Add InfluxDB as a data source
3. Import the provided dashboard template
4. Configure Worldmap panel with appropriate coordinates

#### Streamlit Dashboard
1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit dashboard:
   ```bash
   streamlit run streamlit_dashboard.py
   ```
3. Access the dashboard at http://localhost:8501
4. For Windows users, simply run `run_dashboard.bat`

#### Nairobi Forest Dashboard
1. Install required Python packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Nairobi dashboard:
   ```bash
   streamlit run nairobi_dashboard.py
   ```
3. Access the dashboard at http://localhost:8504
4. For Windows users, simply run `run_nairobi_dashboard.bat`

#### Deforestation Analysis Dashboard
1. Install required Python packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the deforestation analysis dashboard:
   ```bash
   streamlit run deforestation_analysis.py
   ```
3. Access the dashboard at http://localhost:8505
4. For Windows users, simply run `run_deforestation_analysis.bat`

#### Institutional Dashboard
1. Install required Python packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the institutional dashboard:
   ```bash
   streamlit run institutional_dashboard.py
   ```
3. Access the dashboard at http://localhost:8506
4. For Windows users, simply run `run_institutional_dashboard.bat`

#### Research Dashboard
1. Install required Python packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the research dashboard:
   ```bash
   streamlit run research_dashboard.py
   ```
3. Access the dashboard at http://localhost:8507
4. For Windows users, simply run `run_research_dashboard.bat`

#### Policy & Carbon Credit Dashboard
1. Install required Python packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the policy dashboard:
   ```bash
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
| Fire Detection | Crackling Sounds |
| Biodiversity Monitoring | Bird Calls, Animal Sounds |

## Testing

To test the system:
1. Run Raspberry Pi script
2. Place in test environment
3. Play chainsaw audio sample near microphone
4. Verify Telegram alert receipt
5. Check InfluxDB for data
6. Confirm Grafana dashboard updates

## Troubleshooting

- Ensure SIM card has active service and sufficient credit
- Check antenna connection for GSM module
- Verify InfluxDB credentials and network connectivity
- For Raspberry Pi implementation, check LoRa antenna and gateway connectivity