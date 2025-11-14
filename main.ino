#include <WiFi.h>
#include <Wire.h>
#include <driver/i2s.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <HTTPClient.h>
#include "config.h"
#include "edge_impulse_integration.h"

// Pin definitions are now in config.h

// I2S configuration
#define I2S_PORT I2S_NUM_0
#define BUFFER_SIZE 512

// SIM800L serial communication
HardwareSerial sim800l(1);

// GPS object
TinyGPSPlus gps;

// Device configuration is now in config.h

// Audio buffer
int32_t samples[BUFFER_SIZE];
int samples_count = 0;

void setup() {
  Serial.begin(115200);
  
  // Initialize Edge Impulse model
  ei_init();
  
  // Initialize I2S for microphone
  i2sInit();
  
  // Initialize SIM800L
  sim800l.begin(9600, SERIAL_8N1, SIM800L_RX_PIN, SIM800L_TX_PIN);
  delay(1000);
  
  // Wait for SIM800L to initialize
  sim800l.println("AT");
  delay(1000);
  
  // Initialize GPS
  // GPS will be connected to default Serial pins
  
  Serial.println("Acoustic Guardian initialized");
}

void loop() {
  // Read audio samples
  size_t bytes_read;
  esp_err_t result = i2s_read(I2S_PORT, &samples, BUFFER_SIZE * sizeof(int32_t), &bytes_read, portMAX_DELAY);
  
  if (result == ESP_OK) {
    samples_count = bytes_read / sizeof(int32_t);
    
    // Process audio for chainsaw detection
    detection_result_t result = ei_run_inference(samples, samples_count);
    
    if (result.is_chainsaw && result.confidence > DETECTION_THRESHOLD) {
      Serial.print("Chainsaw detected with confidence: ");
      Serial.println(result.confidence);
      
      // Get GPS coordinates
      String gps_coords = getGPSCoordinates();
      String timestamp = getTimestamp();
      
      // Send SMS alert
      sendSMSAlert(gps_coords, timestamp);
      
      // Log data to InfluxDB
      logToInfluxDB(gps_coords, timestamp);
      
      // Wait before next detection to avoid spam
      delay(30000);
    }
  }
  
  // Update GPS
  while (Serial.available() > 0) {
    gps.encode(Serial.read());
  }
  
  delay(10);
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
    .bck_io_num = I2S_SCK_PIN,
    .ws_io_num = I2S_WS_PIN,
    .data_out_num = -1,
    .data_in_num = I2S_SD_PIN
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

bool detectChainsaw(int32_t* samples, int count) {
  // This is a placeholder for the Edge Impulse model inference
  // In practice, you would:
  // 1. Convert samples to float array
  // 2. Run Edge Impulse impulse
  // 3. Check classification results
  // 4. Return true if chainsaw confidence > 90%
  
  // Simulating detection for testing
  static unsigned long last_detection = 0;
  if (millis() - last_detection > 60000) { // Simulate detection every minute for testing
    last_detection = millis();
    return true;
  }
  return false;
}

String getGPSCoordinates() {
  if (gps.location.isValid()) {
    String lat = String(gps.location.lat(), 6);
    String lng = String(gps.location.lng(), 6);
    return lat + "," + lng;
  } else {
    return "0.000000,0.000000"; // Default coordinates if GPS not available
  }
}

String getTimestamp() {
  // Return current timestamp
  return String(millis());
}

void sendSMSAlert(String gps_coords, String timestamp) {
  Serial.println("Sending SMS alert...");
  
  // Configure SMS mode
  sim800l.println("AT+CMGF=1");
  delay(1000);
  
  // Set phone number
  sim800l.print("AT+CMGS=\"");
  sim800l.print(RANGER_PHONE_NUMBER);
  sim800l.println("\"");
  delay(1000);
  
  // Send message
  sim800l.print("ALERT! Chainsaw detected at ");
  sim800l.print(gps_coords);
  sim800l.print(" - ");
  sim800l.println(timestamp);
  sim800l.write(26); // CTRL+Z to send
  
  delay(5000);
  Serial.println("SMS sent!");
}

void logToInfluxDB(String gps_coords, String timestamp) {
  Serial.println("Logging to InfluxDB...");
  
  // Prepare data in InfluxDB line protocol
  String data = "acoustic_guardian,device_id=";
  data += DEVICE_ID;
  data += " gps_coordinates=\"";
  data += gps_coords;
  data += "\",threat_type=\"chainsaw\",confidence=";
  data += "0.95";  // This should come from the detection result
  data += ",threat_detected=true,time_safe=0 ";
  data += String(millis() / 1000); // Unix timestamp
  
  // Send HTTP POST request
  if (sim800l.println("AT+CGATT?") && sim800l.find("OK")) {
    sim800l.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
    delay(1000);
    sim800l.print("AT+SAPBR=3,1,\"APN\",\"");
    sim800l.print(GSM_APN);
    sim800l.println("\""); // Using configured APN
    delay(1000);
    sim800l.println("AT+SAPBR=1,1");
    delay(3000);
    sim800l.println("AT+HTTPINIT");
    delay(2000);
    sim800l.println("AT+HTTPPARA=\"CID\",1");
    delay(1000);
    sim800l.print("AT+HTTPPARA=\"URL\",\"");
    sim800l.print(INFLUXDB_URL);
    sim800l.println("\"");
    delay(1000);
    sim800l.println("AT+HTTPPARA=\"CONTENT\",\"text/plain\"");
    delay(1000);
    sim800l.print("AT+HTTPDATA=");
    sim800l.print(data.length());
    sim800l.println(",10000");
    delay(1000);
    sim800l.println(data);
    delay(1000);
    sim800l.println("AT+HTTPACTION=1"); // POST
    delay(5000);
    sim800l.println("AT+HTTPTERM");
    delay(1000);
    sim800l.println("AT+SAPBR=0,1");
    delay(1000);
    
    Serial.println("Data logged to InfluxDB!");
    Serial.println("Data sent: " + data);
  } else {
    Serial.println("Failed to connect to GPRS");
  }
}
