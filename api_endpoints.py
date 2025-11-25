"""
API endpoints for EcoGuard system
This would be integrated with the existing Streamlit application
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Mock data - in reality this would come from your existing data sources
FORESTS = [
    {
        "id": "1",
        "name": "Karura Forest",
        "location": {"lat": -1.2723, "lng": 36.8080},
        "area": 17.5,
        "type": "Urban Forest",
        "region": "Nairobi"
    },
    {
        "id": "2",
        "name": "Uhuru Park",
        "location": {"lat": -1.3037, "lng": 36.8166},
        "area": 0.6,
        "type": "Urban Park",
        "region": "Nairobi"
    }
]

SENSORS = [
    {
        "id": "AG-001",
        "forestId": "1",
        "status": "active",
        "battery": 95.5,
        "signal": -65,
        "lastDetection": "2023-06-15T10:30:00Z"
    }
]

# Enhanced user roles with organization support
USER_ROLES = {
    'FOREST_RANGER': 'forest_ranger',
    'REGIONAL_MANAGER': 'regional_manager',
    'SUPER_USER': 'super_user'
}

# Mock users with organizations
USERS = {
    "ranger1": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": USER_ROLES['FOREST_RANGER'],
        "name": "John Ranger",
        "organization": "Nairobi Conservation Team",
        "region": "Nairobi"
    },
    "manager1": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": USER_ROLES['REGIONAL_MANAGER'],
        "name": "Sarah Manager",
        "organization": "Central Kenya Forest Authority",
        "region": "Central Kenya"
    },
    "admin": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": USER_ROLES['SUPER_USER'],
        "name": "System Administrator",
        "organization": "EcoGuard Kenya",
        "region": "All Regions"
    }
}

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if username in USERS:
        user = USERS[username]
        if verify_password(password, user["password_hash"]):
            # In a real implementation, you would create a session token here
            return jsonify({
                "user": {
                    "id": username,
                    "name": user["name"],
                    "role": user["role"],
                    "organization": user["organization"],
                    "region": user["region"]
                },
                "token": "mock-jwt-token"  # In reality, this would be a real JWT
            }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    # In a real implementation, you would invalidate the session token here
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/auth/user', methods=['GET'])
def get_user():
    """Get current user info"""
    # In a real implementation, you would validate the session token here
    # For now, we'll return mock data but validate the token exists
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid authorization token"}), 401
    
    # Extract token (in a real app, you would validate it)
    token = auth_header.split(' ')[1]
    
    # For demo purposes, we'll decode the token to get the username
    # In a real app, this would be a proper JWT validation
    # For now, we'll just check if the token matches our mock token
    if token == "mock-jwt-token":
        # Return the ranger1 user data as default
        user = USERS["ranger1"]
        return jsonify({
            "user": {
                "id": "ranger1",
                "name": user["name"],
                "role": user["role"],
                "organization": user["organization"],
                "region": user["region"]
            }
        }), 200
    
    # If we want to support other users, we could implement logic here
    # For now, we'll just return the default user
    user = USERS["ranger1"]
    return jsonify({
        "user": {
            "id": "ranger1",
            "name": user["name"],
            "role": user["role"],
            "organization": user["organization"],
            "region": user["region"]
        }
    }), 200

# Forest data endpoints
@app.route('/api/forests', methods=['GET'])
def get_forests():
    """Get all forests"""
    return jsonify(FORESTS), 200

@app.route('/api/forests/<forest_id>', methods=['GET'])
def get_forest(forest_id):
    """Get specific forest"""
    forest = next((f for f in FORESTS if f["id"] == forest_id), None)
    if forest:
        return jsonify(forest), 200
    return jsonify({"error": "Forest not found"}), 404

# Sensor data endpoints
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """Get all sensors"""
    return jsonify(SENSORS), 200

@app.route('/api/sensors/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """Get specific sensor"""
    sensor = next((s for s in SENSORS if s["id"] == sensor_id), None)
    if sensor:
        return jsonify(sensor), 200
    return jsonify({"error": "Sensor not found"}), 404

@app.route('/api/forests/<forest_id>/sensors', methods=['GET'])
def get_forest_sensors(forest_id):
    """Get sensors for a specific forest"""
    sensors = [s for s in SENSORS if s["forestId"] == forest_id]
    return jsonify(sensors), 200

# Analytics endpoints
@app.route('/api/analytics/risk', methods=['GET'])
def get_risk_data():
    """Get deforestation risk data"""
    # Mock risk data
    risk_data = [
        {"forest": "Karura Forest", "risk_score": 0.67},
        {"forest": "Uhuru Park", "risk_score": 0.93}
    ]
    return jsonify(risk_data), 200

@app.route('/api/analytics/detections', methods=['GET'])
def get_detections():
    """Get detection history"""
    # Mock detection data
    detections = [
        {"timestamp": "2023-06-15T10:30:00Z", "forest": "Karura Forest", "confidence": 94.5},
        {"timestamp": "2023-06-14T15:45:00Z", "forest": "Karura Forest", "confidence": 92.1}
    ]
    return jsonify(detections), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)