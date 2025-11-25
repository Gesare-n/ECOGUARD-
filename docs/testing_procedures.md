# Acoustic Guardian - Testing Procedures

## Component Testing

### 1. INMP441 Microphone Test

Create a simple sketch to verify microphone functionality:

```cpp
#include <driver/i2s.h>

#define I2S_WS 15
#define I2S_SD 13
#define I2S_SCK 2

#define I2S_PORT I2S_NUM_0
#define BUFFER_SIZE 512

int32_t samples[BUFFER_SIZE];

void setup() {
  Serial.begin(115200);
  i2sInit();
  Serial.println("Microphone test started");
}

void loop() {
  size_t bytes_read;
  esp_err_t result = i2s_read(I2S_PORT, &samples, BUFFER_SIZE * sizeof(int32_t), &bytes_read, portMAX_DELAY);
  
  if (result == ESP_OK) {
    int samples_count = bytes_read / sizeof(int32_t);
    Serial.print("Samples read: ");
    Serial.println(samples_count);
    
    // Print first 10 samples
    for (int i = 0; i < 10 && i < samples_count; i++) {
      Serial.println(samples[i]);
    }
  }
  delay(1000);
}

void i2sInit() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = BUFFER_SIZE,
    .use_apll = false
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = -1,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}
```

### 2. SIM800L GSM Module Test

Create a test sketch to verify GSM functionality:

```cpp
#include <HardwareSerial.h>

#define SIM800L_RX 16
#define SIM800L_TX 17

HardwareSerial sim800l(1);

void setup() {
  Serial.begin(115200);
  sim800l.begin(9600, SERIAL_8N1, SIM800L_RX, SIM800L_TX);
  delay(1000);
  
  Serial.println("Testing SIM800L...");
  
  // Test basic communication
  sim800l.println("AT");
  delay(1000);
  if (sim800l.find("OK")) {
    Serial.println("SIM800L responding");
  } else {
    Serial.println("SIM800L not responding");
  }
  
  // Check signal strength
  sim800l.println("AT+CSQ");
  delay(1000);
  while (sim800l.available()) {
    Serial.write(sim800l.read());
  }
  
  // Check network registration
  sim800l.println("AT+CREG?");
  delay(1000);
  while (sim800l.available()) {
    Serial.write(sim800l.read());
  }
}

void loop() {
  // Nothing to do here
}
```

### 3. GPS Module Test

Create a test sketch to verify GPS functionality:

```cpp
#include <TinyGPS++.h>

TinyGPSPlus gps;

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600); // GPS typically communicates at 9600 baud
  Serial.println("GPS test started");
}

void loop() {
  while (Serial2.available() > 0) {
    char c = Serial2.read();
    gps.encode(c);
    
    if (gps.location.isUpdated()) {
      Serial.print("Latitude: ");
      Serial.println(gps.location.lat(), 6);
      Serial.print("Longitude: ");
      Serial.println(gps.location.lng(), 6);
      Serial.print("Satellites: ");
      Serial.println(gps.satellites.value());
    }
  }
}
```

## End-to-End System Testing

### Test Procedure

1. **Audio Detection Test**
   - Play a chainsaw audio sample near the device
   - Verify the device detects the sound and logs to serial monitor
   - Check that confidence level exceeds 90%

2. **SMS Alert Test**
   - After detection, verify SMS is sent to the configured ranger number
   - Check that the message contains GPS coordinates and timestamp

3. **InfluxDB Data Logging Test**
   - Verify data is written to InfluxDB
   - Check that the data contains:
     - Correct device ID
     - Accurate GPS coordinates
     - Proper threat classification
     - Appropriate confidence level
     - Reset "time_safe" metric

4. **Grafana Dashboard Test**
   - Confirm that the Grafana dashboard updates in real-time
   - Verify that:
     - Red hotspot appears on map at sensor location
     - "Time Safe" metric resets to zero
     - Historical and high-risk layers display correctly

### Test Data

Prepare the following test data:

1. Chainsaw audio samples (10-15 seconds each)
2. Nature ambient sounds (for false positive testing)
3. Predefined GPS coordinates for testing
4. Valid phone number for SMS testing

### Expected Results

| Test | Expected Result | Success Criteria |
|------|----------------|------------------|
| Audio Detection | Device identifies chainsaw sound | >90% confidence |
| SMS Alert | Message received within 30 seconds | Contains GPS coords |
| Data Logging | Record appears in InfluxDB | All fields populated |
| Dashboard Update | Grafana shows new data | Map updates in <1 min |

## Troubleshooting Guide

### No Audio Detection
- Check microphone wiring
- Verify power to microphone (3.3V)
- Confirm I2S pin connections
- Test with microphone test sketch

### SMS Not Sending
- Verify SIM card is inserted and active
- Check account balance/plan
- Confirm phone number format
- Test with GSM test sketch

### Data Not Logging to InfluxDB
- Verify InfluxDB credentials
- Check internet connectivity via GPRS
- Confirm APN settings for carrier
- Test HTTP connectivity

### Dashboard Not Updating
- Verify InfluxDB data source in Grafana
- Check query syntax in panels
- Confirm time range settings
- Validate GPS coordinate format