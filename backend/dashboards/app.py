"""
Main application entry point for EcoGuard Forest Protection System
"""

import streamlit as st
import auth

# Set page config
st.set_page_config(
    page_title="EcoGuard - Forest Protection System",
    page_icon="🌳",
    layout="centered"
)

# Initialize session
auth.init_session()

# Check if user is logged in
if auth.is_logged_in():
    # User is logged in, show dashboard options
    user = auth.get_current_user()
    user_role = user['role']
    
    st.title("🌳 EcoGuard Forest Protection System")
    st.markdown(f"### Welcome, {user['name']} ({auth.get_user_role_name(user_role)})")
    
    st.subheader("Select Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Standard Dashboard")
        st.info("View forest monitoring data, detections, and system status")
        if st.button("Launch Standard Dashboard", key="standard"):
            st.switch_page("streamlit_dashboard.py")
    
    with col2:
        st.markdown("### 👤 My Profile")
        st.info("Manage your account settings and password")
        if st.button("Manage Profile", key="profile"):
            st.switch_page("profile.py")
    
    # Show additional options based on user role
    if user_role == 'super_user':
        st.markdown("---")
        st.subheader("Super User Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👥 User Management")
            st.info("Manage system users, roles, and permissions")
            if st.button("Manage Users", key="users"):
                st.switch_page("user_management.py")
        
        with col2:
            st.markdown("### 🛠️ System Administration")
            st.info("System configuration and advanced settings")
            if st.button("System Admin", key="admin"):
                st.info("System administration features would be available here")
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout"):
        auth.logout_user()
        st.success("You have been logged out successfully")
        st.rerun()  # Updated from st.experimental_rerun()
else:
    # User is not logged in, show login page
    st.title("🌳 EcoGuard Forest Protection System")
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                user_info = auth.authenticate_user(username, password)
                if user_info:
                    auth.login_user(user_info)
                    st.success(f"Welcome, {user_info['name']}!")
                    st.rerun()  # Updated from st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    # Demo credentials info
    st.info("""
    **Demo Credentials:**
    - Forest Ranger: username `ranger1`, password `password`
    - Regional Manager: username `manager1`, password `password`
    - Super User: username `admin`, password `password`
    """)