#ifndef CONFIG_H
#define CONFIG_H

// Device Configuration
#define DEVICE_ID "AG-001"  // Unique identifier for this device

// Ranger Contact Information
#define RANGER_PHONE_NUMBER "+1234567890"  // Replace with actual ranger number

// InfluxDB Configuration
#define INFLUXDB_URL "https://your-instance.cloud.influxdata.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s"
#define INFLUXDB_TOKEN "your-token-here"
#define INFLUXDB_ORG "your-org"
#define INFLUXDB_BUCKET "your-bucket"

// GSM Configuration
#define GSM_APN "your-apn"  // Replace with your mobile carrier's APN
#define GSM_GPRS_USER ""
#define GSM_GPRS_PASS ""

// Audio Processing Parameters
#define SAMPLE_RATE 16000
#define AUDIO_BUFFER_SIZE 512
#define DETECTION_THRESHOLD 0.9  // 90% confidence threshold

// GPS Settings
#define GPS_SERIAL_BAUD 9600

// Timing Constants (in milliseconds)
#define DETECTION_INTERVAL 5000      // Time between detections
#define SMS_COOLDOWN 30000           // Minimum time between SMS alerts
#define DATA_LOG_INTERVAL 60000      // Regular data logging interval

// Pin Definitions
// I2S Microphone (INMP441)
#define I2S_WS_PIN 15
#define I2S_SD_PIN 13
#define I2S_SCK_PIN 2

// SIM800L
#define SIM800L_RX_PIN 16
#define SIM800L_TX_PIN 17

#endif // CONFIG_H