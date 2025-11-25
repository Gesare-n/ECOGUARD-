"""
User Management Dashboard for EcoGuard Super Users
"""

import streamlit as st
import pandas as pd
import auth

# Set page config
st.set_page_config(
    page_title="EcoGuard - User Management",
    page_icon="🌳",
    layout="wide"
)

# Initialize session and check authentication
auth.init_session()

if not auth.is_logged_in():
    st.switch_page("login.py")

user = auth.get_current_user()

# Check if user has super user privileges
if user['role'] != 'super_user':
    st.error("Access denied. This page requires Super User privileges.")
    st.stop()

st.title("👥 User Management")
st.markdown("### Manage EcoGuard System Users")

# Load current users
users = auth.load_users()

# Convert to DataFrame for display
users_df = pd.DataFrame.from_dict(users, orient='index')
users_df.reset_index(inplace=True)
users_df.rename(columns={'index': 'username'}, inplace=True)

# Tabs for different functions
tab1, tab2, tab3 = st.tabs(["View Users", "Add User", "Edit User"])

with tab1:
    st.subheader("Current Users")
    st.dataframe(users_df[['username', 'name', 'role', 'region', 'last_login']], use_container_width=True)

with tab2:
    st.subheader("Add New User")
    
    with st.form("add_user_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_name = st.text_input("Full Name")
        new_role = st.selectbox("Role", list(auth.ROLES.keys()), format_func=lambda x: auth.ROLES[x])
        new_region = st.selectbox("Region", ["Nairobi", "Central", "Western", "Rift Valley", "Coastal", "All Regions"])
        
        submitted = st.form_submit_button("Add User")
        
        if submitted:
            if new_username and new_password and new_name:
                success, message = auth.create_user(new_username, new_password, new_name, new_role, new_region)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please fill in all required fields")

with tab3:
    st.subheader("Edit User")
    
    # Select user to edit
    selected_user = st.selectbox("Select User to Edit", list(users.keys()))
    
    if selected_user:
        user_info = users[selected_user]
        
        with st.form("edit_user_form"):
            edit_name = st.text_input("Full Name", value=user_info.get('name', ''))
            # Safely get the index for role selection
            user_role = user_info.get('role', 'forest_ranger')
            role_options = list(auth.ROLES.keys())
            role_index = role_options.index(user_role) if user_role in role_options else 0
            
            edit_role = st.selectbox("Role", role_options, 
                                   index=role_index,
                                   format_func=lambda x: auth.ROLES[x])
            # Safely get the index for region selection
            user_region = user_info.get('region', 'Nairobi')
            region_options = ["Nairobi", "Central", "Western", "Rift Valley", "Coastal", "All Regions"]
            region_index = region_options.index(user_region) if user_region in region_options else 0
            
            edit_region = st.selectbox("Region", region_options,
                                     index=region_index)
            
            submitted = st.form_submit_button("Update User")
            
            if submitted:
                # Update user profile
                if auth.update_user_profile(selected_user, edit_name, edit_region):
                    # Update role in users dict
                    users[selected_user]['name'] = edit_name
                    users[selected_user]['role'] = edit_role
                    users[selected_user]['region'] = edit_region
                    auth.save_users(users)
                    st.success("User updated successfully")
                    st.rerun()
                else:
                    st.error("Failed to update user")

# Logout button in sidebar
if st.sidebar.button("🚪 Logout"):
    auth.logout_user()
    st.switch_page("login.py")

# Sidebar information
st.sidebar.title("EcoGuard")
st.sidebar.markdown(f"**User:** {user['name']}")
st.sidebar.markdown(f"**Role:** {auth.get_user_role_name(user['role'])}")
st.sidebar.markdown(f"**Region:** {user['region']}")

st.sidebar.markdown("### User Management")
st.sidebar.info("This page allows Super Users to manage all system users, including adding new users and modifying existing ones.")

# Footer
st.markdown("---")
st.markdown(f"🌳 EcoGuard - User Management System | User: {user['name']} ({auth.get_user_role_name(user['role'])})")