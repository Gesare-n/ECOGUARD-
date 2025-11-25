"""
Authentication module for EcoGuard Forest Protection System
Provides user authentication, session management, and role-based access control
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# User roles
ROLES = {
    'forest_ranger': 'Forest Ranger',
    'regional_manager': 'Regional Manager', 
    'super_user': 'Super User'
}

# Default users (in a real application, this would be stored in a database)
DEFAULT_USERS = {
    "ranger1": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": "forest_ranger",
        "name": "John Ranger",
        "region": "Nairobi",
        "last_login": None
    },
    "manager1": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": "regional_manager",
        "name": "Sarah Manager",
        "region": "Central Kenya",
        "last_login": None
    },
    "admin": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password: password
        "role": "super_user",
        "name": "System Administrator",
        "region": "All Regions",
        "last_login": None
    }
}

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def load_users():
    """Load users from file or return defaults"""
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                # Load and return the users, but if there's an error return defaults
                data = json.load(f)
                # Ensure all default users are present
                for user, details in DEFAULT_USERS.items():
                    if user not in data:
                        data[user] = details
                return data
        except Exception as e:
            print(f"Error loading users file: {e}")
            return DEFAULT_USERS
    return DEFAULT_USERS

def save_users(users):
    """Save users to file"""
    try:
        with open("users.json", 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users file: {e}")
        return False

def authenticate_user(username, password):
    """Authenticate a user and return user info if successful"""
    users = load_users()
    if username in users:
        user = users[username]
        if "password_hash" in user and verify_password(password, user["password_hash"]):
            # Update last login
            user["last_login"] = datetime.now().isoformat()
            save_users(users)
            return {
                "username": username,
                "name": user["name"],
                "role": user["role"],
                "region": user["region"],
                "last_login": user["last_login"]
            }
    return None

def create_user(username, password, name, role, region):
    """Create a new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    if role not in ROLES:
        return False, "Invalid role"
    
    users[username] = {
        "password_hash": hash_password(password),
        "role": role,
        "name": name,
        "region": region,
        "last_login": None
    }
    
    if save_users(users):
        return True, "User created successfully"
    else:
        return False, "Failed to save user data"

def update_user_profile(username, name=None, region=None):
    """Update user profile information"""
    users = load_users()
    if username in users:
        if name:
            users[username]["name"] = name
        if region:
            users[username]["region"] = region
        return save_users(users)
    return False

def change_password(username, old_password, new_password):
    """Change user password"""
    users = load_users()
    if username in users:
        user = users[username]
        if "password_hash" in user and verify_password(old_password, user["password_hash"]):
            user["password_hash"] = hash_password(new_password)
            if save_users(users):
                return True, "Password changed successfully"
            else:
                return False, "Failed to save password change"
        else:
            return False, "Current password is incorrect"
    return False, "User not found"

def get_user_role_name(role_key):
    """Get the display name for a role key"""
    return ROLES.get(role_key, "Unknown Role")

def require_role(required_roles):
    """Decorator to require specific roles for access"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user' not in st.session_state:
                st.warning("You must be logged in to access this page")
                return None
            if st.session_state.user['role'] not in required_roles:
                st.warning(f"Access denied. This page requires {', '.join([ROLES.get(r, r) for r in required_roles])} privileges.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Session management functions
def init_session():
    """Initialize session state for authentication"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def login_user(user_info):
    """Login a user"""
    st.session_state.user = user_info
    st.session_state.authenticated = True

def logout_user():
    """Logout the current user"""
    st.session_state.user = None
    st.session_state.authenticated = False

def is_logged_in():
    """Check if a user is logged in"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get the current logged in user"""
    return st.session_state.get('user', None)

def get_user_role():
    """Get the role of the current user"""
    user = get_current_user()
    if user:
        return user.get('role', None)
    return None