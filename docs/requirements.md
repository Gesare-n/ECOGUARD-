# Acoustic Guardian - Required Libraries and Dependencies

## Arduino IDE Libraries

These libraries need to be installed through the Arduino IDE Library Manager:

1. TinyGPS++ by Mikal Hart
2. WiFi by Arduino
3. HTTPClient by Arduino
4. HardwareSerial by Arduino

## Edge Impulse Model Library

After training your model on Edge Impulse Studio:
1. Go to Deployment tab
2. Select "Arduino library"
3. Download and install the library in your Arduino libraries folder

## PlatformIO Dependencies (if using PlatformIO instead of Arduino IDE)

Add these to your `platformio.ini` file:

```
lib_deps =
    mikalhart/TinyGPSPlus@^1.0.2
    edgeimpulse/Edge Impulse Arduino SDK@^1.0.0
```

## InfluxDB Cloud

1. Sign up at https://cloud.influxdata.com/
2. Create an organization and bucket
3. Generate an API token with write permissions

## Grafana Cloud

1. Sign up at https://grafana.com/products/cloud/
2. Set up a Grafana instance
3. Add InfluxDB as a data source

## Hardware Components

1. TTGO T-Call ESP32 SIM800L Development Board
2. INMP441 I2S MEMS Microphone
3. SIM Card with active data plan
4. Antenna for GSM connectivity
5. Power source (battery pack or solar panel setup)

## Mobile Carrier Requirements

1. GSM/GPRS compatible carrier
2. Active data plan for GPRS connectivity
3. SMS enabled on the SIM card

## Development Environment

1. Arduino IDE 1.8.15 or higher
2. ESP32 Board Package (version 1.0.6 or higher)
3. USB cable for programming
4. Serial monitor for debugging

## Testing Equipment

1. Audio playback device for testing chainsaw sound samples
2. GPS simulator or outdoor testing area with clear sky view
3. Mobile phone to receive SMS alerts