# Acoustic Guardian - Field Deployment Guide

## Site Selection

### Optimal Placement Criteria
1. **Sound Coverage**: Position to maximize detection area for chainsaw noise
2. **GSM Signal**: Ensure clear line of sight to cellular towers
3. **Weather Protection**: Shield from direct rain and extreme temperatures
4. **Accessibility**: Allow for maintenance while preventing tampering
5. **Power Source**: Proximity to solar charging or battery replacement point

### Recommended Mounting Height
- **Minimum**: 2 meters above ground
- **Optimal**: 3-5 meters above ground
- **Maximum**: 10 meters (beyond this, sound detection effectiveness decreases)

## Installation Steps

### 1. Pre-deployment Preparation
- Program device with latest firmware
- Configure device ID and ranger contact information
- Test all components (microphone, GSM, GPS) before deployment
- Fully charge battery or verify solar panel functionality

### 2. Physical Installation
1. **Mounting Pole Setup**
   - Install pole securely in ground (minimum 30cm depth)
   - Ensure pole is vertical and stable
   - Use concrete footing if soil is loose

2. **Device Attachment**
   - Secure device to pole using weatherproof enclosure
   - Orient microphone away from wind direction
   - Point GSM antenna vertically for optimal signal
   - Ensure GPS module has clear view of sky

3. **Cable Management**
   - Route all cables through protective conduit
   - Secure cables to prevent movement in wind
   - Seal all connections against moisture ingress

### 3. Power Connection
1. **Solar Panel Setup** (if applicable)
   - Angle panel toward equator (south in northern hemisphere)
   - Tilt at latitude angle plus 10-15 degrees
   - Clean panel surface regularly

2. **Battery Connection**
   - Connect battery to charge controller
   - Verify proper voltage levels
   - Set low voltage disconnect thresholds

### 4. Network Configuration
1. **SIM Card Installation**
   - Insert SIM card with active data plan
   - Verify PIN status (disable PIN if required)
   - Confirm APN settings for local carrier

2. **Signal Testing**
   - Power on device and check GSM registration
   - Verify signal strength (> -85dBm recommended)
   - Test GPRS connectivity to InfluxDB

## Initial Configuration

### Device Setup
1. Configure device ID in [config.h](file:///D:/AcousticGuardian/config.h) file
2. Set ranger phone number for SMS alerts
3. Update InfluxDB credentials and endpoint
4. Configure APN settings for local carrier
5. Set detection sensitivity thresholds

### Testing at Deployment Site
1. **Functionality Test**
   - Play test audio to verify detection capability
   - Confirm GPS fix and coordinate accuracy
   - Send test SMS to ranger number
   - Verify data transmission to InfluxDB

2. **Network Test**
   - Monitor signal strength over 24 hours
   - Verify consistent data transmission
   - Check battery consumption rates

## Maintenance Schedule

### Weekly Checks
- Visual inspection of mounting hardware
- Check for physical damage or tampering
- Verify indicator lights (if equipped)
- Confirm device is powered on

### Monthly Maintenance
- Clean microphone and solar panel surfaces
- Check and tighten all mounting hardware
- Inspect cables for damage or wear
- Verify battery charge levels
- Test SMS alert functionality

### Quarterly Service
- Full system diagnostics
- Firmware update if available
- Replace batteries if needed
- Professional calibration if detection accuracy degrades

## Troubleshooting at Deployment Site

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| No detection | Microphone blocked | Clear obstruction, reposition |
| SMS failures | Poor signal | Relocate antenna, check SIM |
| No data logging | Network issues | Verify APN, check credits |
| False positives | Wind noise | Adjust sensitivity, relocate |
| Device offline | Power failure | Check solar/battery, connections |

### Diagnostic Commands
Send these SMS commands to the device for remote diagnostics:
- `STATUS` - Returns battery level, signal strength, last detection time
- `LOCATION` - Returns current GPS coordinates
- `TEST` - Runs self-diagnostic and reports results
- `RESET` - Reboots the device

## Security Considerations

### Physical Security
- Use tamper-proof enclosures
- Install at height to prevent easy access
- Apply security screws where possible
- Consider camouflage for sensitive locations

### Data Security
- Use secure InfluxDB authentication
- Enable encryption for data transmission
- Regularly rotate API tokens
- Restrict dashboard access with strong passwords

## Environmental Impact

### Minimizing Footprint
- Use renewable energy sources (solar)
- Select recyclable materials for enclosures
- Minimize ground disturbance during installation
- Plan for end-of-life device recovery

### Wildlife Considerations
- Avoid placement in animal migration corridors
- Minimize light pollution (use infrared indicators)
- Reduce electromagnetic interference
- Schedule maintenance during low-activity periods

## Documentation Requirements

### Site Records
- GPS coordinates of installation
- Photos of installation site and device
- Local contact information for maintenance
- Access permissions and landowner agreements
- Emergency retrieval procedures

### Performance Tracking
- Detection accuracy logs
- Battery performance data
- Network reliability statistics
- Maintenance activity records
- False positive/negative reports

## Retrieval Procedure

### End of Deployment
1. Notify monitoring station of retrieval
2. Collect all components (device, solar panel, batteries)
3. Document condition of equipment
4. Update inventory records
5. Transport to maintenance facility for servicing

### Emergency Retrieval
1. Contact local authorities if device compromised
2. Document any tampering or damage
3. Preserve evidence if theft suspected
4. Report incident to project coordinator