#include "edge_impulse_integration.h"
#include "config.h"
#include <Arduino.h>

// Include Edge Impulse library (uncomment when you have your model)
// #include <model-parameters/model_metadata.h>
// #include <edge-impulse-sdk/classifier/ei_run_classifier.h>

// Signal structure for Edge Impulse
// static ei_impulse_result_t result;

void ei_init() {
  // Initialize Edge Impulse model
  // This would typically involve setting up the DSP and classifier
  // EI_IMPULSE_ERROR init_result = ei_init_classifier();
  // if (init_result != EI_IMPULSE_OK) {
  //   Serial.println("Failed to initialize Edge Impulse classifier");
  // } else {
  //   Serial.println("Edge Impulse classifier initialized");
  // }
  
  // For now, just print a message
  Serial.println("Edge Impulse integration initialized (model not yet connected)");
}

detection_result_t ei_run_inference(int32_t* samples, int count) {
  detection_result_t detection;
  detection.is_chainsaw = false;
  detection.confidence = 0.0;
  detection.timestamp = millis();
  
  // This is where you would run the actual Edge Impulse inference
  // For now, we'll simulate detection for testing purposes
  
  // Convert samples to float array
  // float float_samples[AUDIO_BUFFER_SIZE];
  // convert_samples_to_float(samples, float_samples, count);
  
  // Create signal from samples
  // signal_t signal;
  // EI_IMPULSE_ERROR ei_result = numpy::signal_from_buffer(float_samples, count, &signal);
  
  // Run classifier
  // EI_IMPULSE_ERROR classify_result = run_classifier(&signal, &result, false);
  
  // if (classify_result != EI_IMPULSE_OK) {
  //   Serial.println("ERR: Failed to classify audio");
  //   return detection;
  // }
  
  // Check results
  // for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
  //   if (result.classification[ix].value > DETECTION_THRESHOLD) {
  //     if (strcmp(result.classification[ix].label, "chainsaw") == 0) {
  //       detection.is_chainsaw = true;
  //       detection.confidence = result.classification[ix].value;
  //       Serial.print("Chainsaw detected with confidence: ");
  //       Serial.println(detection.confidence);
  //       break;
  //     }
  //   }
  // }
  
  // Simulate detection for testing
  static unsigned long last_detection = 0;
  if (millis() - last_detection > 60000) { // Simulate detection every minute for testing
    last_detection = millis();
    detection.is_chainsaw = true;
    detection.confidence = 0.95; // Above our 90% threshold
    Serial.println("SIMULATED: Chainsaw detected with 95% confidence");
  }
  
  return detection;
}

void convert_samples_to_float(int32_t* input, float* output, int count) {
  // Convert 32-bit I2S samples to float values
  for (int i = 0; i < count; i++) {
    // I2S samples are 32-bit but the actual data is in the upper bits
    // Extract the 24-bit value and convert to float
    int32_t sample = input[i] >> 8; // Right shift to get 24-bit value
    
    // Convert to float in range -1.0 to 1.0
    output[i] = (float)sample / 8388608.0; // 2^23
  }
}