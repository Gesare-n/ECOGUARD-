#!/usr/bin/env python3
"""
Configuration file for Raspberry Pi-based Acoustic Guardian with LoRa communication
"""

import os

# Device Configuration
DEVICE_ID = os.getenv("DEVICE_ID", "AG-HB-001")  # Digital Hummingbird identifier
DEVICE_NAME = os.getenv("DEVICE_NAME", "Digital Hummingbird")

# Ranger Contact Information
RANGER_PHONE_NUMBER = os.getenv("RANGER_PHONE_NUMBER", "+2547XXXXXXXX")  # Replace with actual ranger number

# InfluxDB Configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "your-token-here")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "your-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "your-bucket")

# LoRa Configuration
LORA_FREQUENCY = float(os.getenv("LORA_FREQUENCY", "868.1"))  # MHz
LORA_SPREADING_FACTOR = int(os.getenv("LORA_SPREADING_FACTOR", "7"))
LORA_BANDWIDTH = int(os.getenv("LORA_BANDWIDTH", "125000"))  # Hz
LORA_CODING_RATE = int(os.getenv("LORA_CODING_RATE", "5"))
LORA_SYNC_WORD = int(os.getenv("LORA_SYNC_WORD", "0x12"), 16)

# GSM Configuration (for SMS alerts)
GSM_APN = os.getenv("GSM_APN", "your-apn")  # Replace with your mobile carrier's APN
GSM_GPRS_USER = os.getenv("GSM_GPRS_USER", "")
GSM_GPRS_PASS = os.getenv("GSM_GPRS_PASS", "")

# Audio Processing Parameters
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
AUDIO_BUFFER_SIZE = int(os.getenv("AUDIO_BUFFER_SIZE", "512"))
DETECTION_THRESHOLD = float(os.getenv("DETECTION_THRESHOLD", "0.9"))  # 90% confidence threshold

# Camera Processing Parameters
CAMERA_RESOLUTION_WIDTH = int(os.getenv("CAMERA_RESOLUTION_WIDTH", "640"))
CAMERA_RESOLUTION_HEIGHT = int(os.getenv("CAMERA_RESOLUTION_HEIGHT", "480"))
CAMERA_RESOLUTION = (CAMERA_RESOLUTION_WIDTH, CAMERA_RESOLUTION_HEIGHT)
CAMERA_FPS = int(os.getenv("CAMERA_FPS", "30"))

# Timing Constants (in seconds)
DETECTION_INTERVAL = int(os.getenv("DETECTION_INTERVAL", "5"))  # Time between detections
SMS_COOLDOWN = int(os.getenv("SMS_COOLDOWN", "30"))  # Minimum time between SMS alerts
DATA_LOG_INTERVAL = int(os.getenv("DATA_LOG_INTERVAL", "60"))  # Regular data logging interval
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "300"))  # Regular heartbeat (5 minutes)

# Pin Definitions for Raspberry Pi
# Audio pins (using USB microphone or I2S)
AUDIO_INPUT_DEVICE = int(os.getenv("AUDIO_INPUT_DEVICE", "0"))  # Default audio input device

# LoRa pins (adjust based on your LoRa module)
LORA_CS_PIN = int(os.getenv("LORA_CS_PIN", "18"))
LORA_RST_PIN = int(os.getenv("LORA_RST_PIN", "14"))
LORA_IRQ_PIN = int(os.getenv("LORA_IRQ_PIN", "26"))

# Camera pins (using Pi Camera or USB camera)
CAMERA_DEVICE = int(os.getenv("CAMERA_DEVICE", "0"))  # Default camera device

# GPS Settings (if using GPS module)
GPS_SERIAL_PORT = os.getenv("GPS_SERIAL_PORT", "/dev/ttyS0")
GPS_BAUD_RATE = int(os.getenv("GPS_BAUD_RATE", "9600"))

# Bird Enclosure Design
ENCLOSURE_TYPE = os.getenv("ENCLOSURE_TYPE", "Transparent Bird")
ENCLOSURE_MATERIAL = os.getenv("ENCLOSURE_MATERIAL", "Weatherproof PLA")
ENCLOSURE_COLOR = os.getenv("ENCLOSURE_COLOR", "Clear with Green Accents")

# AI Model Paths
ACOUSTIC_MODEL_PATH = os.getenv("ACOUSTIC_MODEL_PATH", "models/chainsaw_detection.tflite")
VISUAL_MODEL_PATH = os.getenv("VISUAL_MODEL_PATH", "models/tree_health_classifier.tflite")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "acoustic_guardian.log")

# Network Configuration
GATEWAY_IP = os.getenv("GATEWAY_IP", "192.168.1.100")  # LoRa Gateway IP
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "1680"))  # LoRa Gateway Port

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")