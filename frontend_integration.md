# EcoGuard Frontend Integration Guide

This document explains how to integrate the modern React frontend with the existing Streamlit system.

## Current Architecture

The EcoGuard system currently uses:
- **Streamlit** for the web interface
- **Python** for backend logic
- **InfluxDB** for time-series data storage
- **Grafana** for advanced dashboards
- **Twilio** for SMS alerts

## Proposed Hybrid Architecture

To gradually transition to the modern frontend while maintaining the existing functionality:

### 1. API Layer
Create RESTful API endpoints in the Python backend to serve data to the React frontend:

```python
# Example API endpoint structure
@app.route('/api/auth/login', methods=['POST'])
def login():
    # Handle authentication
    pass

@app.route('/api/forests', methods=['GET'])
def get_forests():
    # Return forest data
    pass

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    # Return sensor data
    pass
```

### 2. Authentication Bridge
Create a shared authentication system between Streamlit and React:

```python
# Shared session management
class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id):
        # Create session token
        pass
    
    def validate_session(self, token):
        # Validate session token
        pass
```

### 3. Data Services
Create data services that both frontends can use:

```python
# Data service layer
class ForestDataService:
    def get_forest_data(self):
        # Fetch forest data from InfluxDB
        pass
    
    def get_sensor_data(self):
        # Fetch sensor data
        pass
    
    def get_deforestation_risk(self):
        # Calculate risk scores
        pass
```

## Integration Steps

### Phase 1: Backend API Development
1. Create Flask/FastAPI endpoints for existing Streamlit functionality
2. Implement shared authentication system
3. Expose forest, sensor, and user data through APIs

### Phase 2: Frontend Development
1. Implement React components using the new API
2. Create authentication flow
3. Build dashboard components (maps, charts, tables)

### Phase 3: Gradual Migration
1. Redirect specific pages from Streamlit to React
2. Maintain both interfaces during transition
3. Deprecate Streamlit pages as React equivalents are completed

## Benefits of Hybrid Approach

### For Users
- Seamless transition with no downtime
- Access to modern UI features
- Improved performance and responsiveness
- Better mobile experience

### For Developers
- Gradual migration reduces risk
- Ability to maintain existing functionality
- Modern development practices
- Better testing and debugging capabilities

## Technical Implementation

### 1. API Endpoints Needed

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/user` - Get current user info

#### Forest Data
- `GET /api/forests` - List all forests
- `GET /api/forests/{id}` - Get specific forest details
- `GET /api/forests/{id}/sensors` - Get sensors for a forest

#### Sensor Data
- `GET /api/sensors` - List all sensors
- `GET /api/sensors/{id}` - Get specific sensor data
- `GET /api/sensors/{id}/status` - Get sensor status

#### Analytics
- `GET /api/analytics/risk` - Deforestation risk scores
- `GET /api/analytics/detections` - Detection history
- `GET /api/analytics/reports` - Generated reports

### 2. Data Models

```typescript
// User model
interface User {
  id: string;
  name: string;
  email: string;
  role: 'ranger' | 'manager' | 'admin';
  region: string;
}

// Forest model
interface Forest {
  id: string;
  name: string;
  location: { lat: number; lng: number };
  area: number; // in km²
  type: string;
  region: string;
}

// Sensor model
interface Sensor {
  id: string;
  forestId: string;
  status: 'active' | 'warning' | 'offline';
  battery: number; // percentage
  signal: number; // dBm
  lastDetection: Date | null;
}
```

### 3. Authentication Flow

1. User logs in through React frontend
2. Credentials sent to `/api/auth/login`
3. Server validates and returns JWT token
4. Token stored in localStorage/cookies
5. Token sent with each subsequent API request
6. Server validates token before processing requests

## Migration Strategy

### Short-term (1-2 months)
- Implement API layer in existing Python code
- Create basic React components
- Set up authentication bridge

### Medium-term (3-6 months)
- Migrate dashboard pages to React
- Implement role-based access control
- Add real-time data features

### Long-term (6+ months)
- Full migration to React frontend
- Deprecate Streamlit interface
- Enhanced features and mobile app

## Deployment Considerations

### Development Environment
- Use Vite for React development
- Set up proxy for API requests during development
- Shared development database for both frontends

### Production Deployment
- Serve React app statically
- API endpoints served by Python backend
- Shared authentication session storage
- Load balancing for high availability

## Testing Strategy

### Unit Testing
- Test React components in isolation
- Test API endpoints with mock data
- Test authentication flows

### Integration Testing
- Test data flow between React and Python
- Test role-based access control
- Test error handling

### End-to-End Testing
- Test complete user workflows
- Test cross-browser compatibility
- Test mobile responsiveness

## Conclusion

This hybrid approach allows for a smooth transition from the current Streamlit interface to a modern React frontend while maintaining all existing functionality. The gradual migration reduces risk and allows users to continue using the system during the transition period.