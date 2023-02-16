import streamlit as st

def login():
    """Streamlit Login App"""

    # Define username and password
    USERNAME = 'user'
    PASSWORD = 'pass'

    # Set page title
    st.set_page_config(page_title='Login App')

    # Create login form
    st.write('Please enter your credentials to log in:')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    login_button = st.button('Login')

    # Check if login button is clicked
    if login_button:
        # Check if username and password are correct
        if username == USERNAME and password == PASSWORD:
            st.success('Logged in as {}'.format(username))
            return True
        else:
            st.error('Invalid credentials')
    return False

### this should go inside separate modeule dashboard.py
import streamlit as st
from login_module import login

def dashboard():
    """Streamlit Dashboard App"""
    if not login():
        st.warning('Please log in to access the dashboard')
        return

    st.set_page_config(page_title='Dashboard App')

    # Add your Streamlit dashboard code here
    st.write('Welcome to the dashboard!')
