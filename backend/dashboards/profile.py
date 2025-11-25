"""
User Profile Management for EcoGuard
"""

import streamlit as st
import auth

# Set page config
st.set_page_config(
    page_title="EcoGuard - Profile",
    page_icon="🌳",
    layout="centered"
)

# Initialize session and check authentication
auth.init_session()

if not auth.is_logged_in():
    st.switch_page("login.py")

user = auth.get_current_user()

st.title("👤 User Profile")
st.markdown("### Manage Your Account Settings")

# Display user information
st.subheader("Account Information")
st.markdown(f"**Username:** {user['username']}")
st.markdown(f"**Name:** {user['name']}")
st.markdown(f"**Role:** {auth.get_user_role_name(user['role'])}")
st.markdown(f"**Region:** {user['region']}")
st.markdown(f"**Last Login:** {user['last_login'] or 'Never'}")

# Change password section
st.subheader("Change Password")

with st.form("change_password_form"):
    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    submitted = st.form_submit_button("Change Password")
    
    if submitted:
        if old_password and new_password and confirm_password:
            if new_password == confirm_password:
                success, message = auth.change_password(user['username'], old_password, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("New passwords do not match")
        else:
            st.warning("Please fill in all password fields")

# Logout button
if st.button("🚪 Logout"):
    auth.logout_user()
    st.switch_page("login.py")

# Sidebar information
st.sidebar.title("EcoGuard")
st.sidebar.markdown(f"**User:** {user['name']}")
st.sidebar.markdown(f"**Role:** {auth.get_user_role_name(user['role'])}")
st.sidebar.markdown(f"**Region:** {user['region']}")

st.sidebar.markdown("### Profile Management")
st.sidebar.info("Update your account settings and change your password securely.")

# Footer
st.markdown("---")
st.markdown(f"🌳 EcoGuard - Profile Management | User: {user['name']} ({auth.get_user_role_name(user['role'])})")