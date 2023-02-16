import streamlit as st
from streamlit_authenticator import SessionState, setup_auth

# set up authentication
setup_auth()

# get the session state object or create a new one
session_state = SessionState.get(name='', email='', password='', is_authenticated=False)

# display the login form
if not session_state.is_authenticated:
    st.write("Please login or register to access the dashboard")
    if st.button("Register"):
        register()
    st.write("Or")
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        if login(email, password):
            session_state.is_authenticated = True
            session_state.name = get_user_name(email)
            session_state.email = email
        else:
            st.error("Incorrect email or password")

# configure the page settings if the user is authenticated
if session_state.is_authenticated:
    st.set_page_config(page_title="My Dashboard", page_icon=":chart_with_upwards_trend:")
    st.write(f"Welcome {session_state.name} ({session_state.email})")
    st.write("Dashboard content goes here")
    if st.button("Logout"):
        session_state.is_authenticated = False
