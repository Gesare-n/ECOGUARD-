#ifndef EDGE_IMPULSE_INTEGRATION_H
#define EDGE_IMPULSE_INTEGRATION_H

// Include Edge Impulse library
// You'll need to install the library from Edge Impulse Studio after training your model
// #include <model-parameters/model_metadata.h>
// #include <edge-impulse-sdk/classifier/ei_run_classifier.h>

// Structure to hold classification results
typedef struct {
  bool is_chainsaw;
  float confidence;
  float timestamp;
} detection_result_t;

/**
 * Initialize the Edge Impulse model
 * This function should be called once during setup
 */
void ei_init();

/**
 * Run inference on audio samples
 * @param samples Audio samples to analyze
 * @param count Number of samples
 * @return Detection result with classification and confidence
 */
detection_result_t ei_run_inference(int32_t* samples, int count);

/**
 * Convert I2S samples to float array for Edge Impulse
 * @param input I2S samples (32-bit)
 * @param output Float array for processing
 * @param count Number of samples
 */
void convert_samples_to_float(int32_t* input, float* output, int count);

#endif // EDGE_IMPULSE_INTEGRATION_H