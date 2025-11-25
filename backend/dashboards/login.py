"""
Login page for EcoGuard Forest Protection System
"""

import streamlit as st
import auth

def show_login_page():
    """Display the login page"""
    st.set_page_config(
        page_title="EcoGuard - Login",
        page_icon="🌳",
        layout="centered"
    )
    
    # Initialize session
    auth.init_session()
    
    # If already logged in, redirect to main dashboard
    if auth.is_logged_in():
        st.switch_page("streamlit_dashboard.py")
    
    # Login form
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
                    st.switch_page("streamlit_dashboard.py")
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

if __name__ == "__main__":
    show_login_page()