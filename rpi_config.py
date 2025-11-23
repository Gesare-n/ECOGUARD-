#!/usr/bin/env python3
"""
Configuration file for Raspberry Pi-based Acoustic Guardian with LoRa communication
"""

# Device Configuration
DEVICE_ID = "AG-HB-001"  # Digital Hummingbird identifier
DEVICE_NAME = "Digital Hummingbird"

# Ranger Contact Information
RANGER_PHONE_NUMBER = "+2547XXXXXXXX"  # Replace with actual ranger number

# InfluxDB Configuration
INFLUXDB_URL = "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s"
INFLUXDB_TOKEN = "your-token-here"
INFLUXDB_ORG = "your-org"
INFLUXDB_BUCKET = "your-bucket"

# LoRa Configuration
LORA_FREQUENCY = 868.1  # MHz
LORA_SPREADING_FACTOR = 7
LORA_BANDWIDTH = 125000  # Hz
LORA_CODING_RATE = 5
LORA_SYNC_WORD = 0x12

# GSM Configuration (for SMS alerts)
GSM_APN = "your-apn"  # Replace with your mobile carrier's APN
GSM_GPRS_USER = ""
GSM_GPRS_PASS = ""

# Audio Processing Parameters
SAMPLE_RATE = 16000
AUDIO_BUFFER_SIZE = 512
DETECTION_THRESHOLD = 0.9  # 90% confidence threshold

# Camera Processing Parameters
CAMERA_RESOLUTION = (640, 480)
CAMERA_FPS = 30

# Timing Constants (in seconds)
DETECTION_INTERVAL = 5  # Time between detections
SMS_COOLDOWN = 30  # Minimum time between SMS alerts
DATA_LOG_INTERVAL = 60  # Regular data logging interval
HEARTBEAT_INTERVAL = 300  # Regular heartbeat (5 minutes)

# Pin Definitions for Raspberry Pi
# Audio pins (using USB microphone or I2S)
AUDIO_INPUT_DEVICE = 0  # Default audio input device

# LoRa pins (adjust based on your LoRa module)
LORA_CS_PIN = 18
LORA_RST_PIN = 14
LORA_IRQ_PIN = 26

# Camera pins (using Pi Camera or USB camera)
CAMERA_DEVICE = 0  # Default camera device

# GPS Settings (if using GPS module)
GPS_SERIAL_PORT = "/dev/ttyS0"
GPS_BAUD_RATE = 9600

# Bird Enclosure Design
ENCLOSURE_TYPE = "Transparent Bird"
ENCLOSURE_MATERIAL = "Weatherproof PLA"
ENCLOSURE_COLOR = "Clear with Green Accents"

# AI Model Paths
ACOUSTIC_MODEL_PATH = "models/chainsaw_detection.tflite"
VISUAL_MODEL_PATH = "models/tree_health_classifier.tflite"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "acoustic_guardian.log"

# Network Configuration
GATEWAY_IP = "192.168.1.100"  # LoRa Gateway IP
GATEWAY_PORT = 1680  # LoRa Gateway Port