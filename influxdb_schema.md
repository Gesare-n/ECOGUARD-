# InfluxDB Schema for Acoustic Guardian

## Bucket Name
`acoustic-guardian`

## Measurements

### 1. acoustic_guardian
Main measurement for threat detection events

Fields:
- `gps_coordinates` (string): Latitude and longitude in format "lat,lng"
- `threat_type` (string): Type of threat detected (e.g., "chainsaw")
- `confidence` (float): Confidence level of detection (0.0 - 1.0)
- `device_id` (string): Unique identifier of the device
- `threat_detected` (boolean): Whether a threat was detected
- `time_safe` (integer): Seconds since last threat detection (resets to 0 when threat detected)

Tags:
- `device_id` (string): Unique identifier of the device
- `location` (string): General location name for the device

Example data point:
```
acoustic_guardian,device_id=AG-001,location=Amazon-Brazil gps_coordinates="-3.4653, -62.2159",threat_type="chainsaw",confidence=0.95,threat_detected=true,time_safe=0 1634567890
```

### 2. device_status
Periodic status updates from devices

Fields:
- `battery_level` (float): Battery level as percentage (0.0 - 100.0)
- `signal_strength` (integer): GSM signal strength in dBm
- `uptime` (integer): Device uptime in seconds

Tags:
- `device_id` (string): Unique identifier of the device

Example data point:
```
device_status,device_id=AG-001 battery_level=87.5,signal_strength=-75,uptime=86400 1634567890
```

## Retention Policies

### Main Data
- Name: `autogen`
- Duration: 90 days
- Shard Group Duration: 1 week

### Long-term Analytics
- Name: `analytics`
- Duration: 365 days
- Shard Group Duration: 1 month
- Replication: 1

## Continuous Queries

### 1. Daily Threat Summary
```sql
CREATE CONTINUOUS QUERY "daily_threat_summary" ON "acoustic-guardian"
RESAMPLE EVERY 1h FOR 25h
BEGIN
  SELECT count(threat_detected) AS threat_count, mean(confidence) AS avg_confidence
  INTO "acoustic-guardian"."analytics"."daily_threats"
  FROM "acoustic-guardian"."autogen"."acoustic_guardian"
  WHERE threat_detected = true
  GROUP BY time(1d), device_id
END
```

### 2. Time Safe Aggregation
```sql
CREATE CONTINUOUS QUERY "time_safe_agg" ON "acoustic-guardian"
RESAMPLE EVERY 1h FOR 25h
BEGIN
  SELECT max(time_safe) AS max_time_safe, min(time_safe) AS min_time_safe
  INTO "acoustic-guardian"."analytics"."time_safe_stats"
  FROM "acoustic-guardian"."autogen"."acoustic_guardian"
  GROUP BY time(1d), device_id
END
```

## Dashboard Queries

### Current Sensor Locations
```flux
from(bucket: "acoustic-guardian")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "acoustic_guardian" and r._field == "gps_coordinates")
  |> last()
```

### Time Safe Metric
```flux
from(bucket: "acoustic-guardian")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "acoustic_guardian" and r._field == "time_safe")
  |> last()
```

### Threat Detection Timeline
```flux
from(bucket: "acoustic-guardian")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "acoustic_guardian" and r._field == "threat_detected")
```

### Device Battery Levels
```flux
from(bucket: "acoustic-guardian")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "device_status" and r._field == "battery_level")
  |> last()
```