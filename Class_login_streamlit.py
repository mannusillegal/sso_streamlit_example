import streamlit as st
import streamlit_authenticator as auth
import mysql.connector

class MyDashboard:
    def __init__(self):
        self.config = {
            'page_title': 'My Dashboard',
            'page_icon': 'icon.png',
            'page_size': (800, 600)
        }
        self.db = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="yourdatabase"
        )
    
    def login(self):
        st.write("## Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            cursor = self.db.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                auth.set_user(user[0])
                st.success("Logged in as {}".format(username))
            else:
                st.error("Invalid username or password")
    
    def register(self):
        st.write("## Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            cursor = self.db.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            try:
                cursor.execute(query, (username, password))
                self.db.commit()
                st.success("Registration successful")
            except:
                st.error("Registration failed")
    
    def reset_password(self):
        st.write("## Reset Password")
        username = st.text_input("Username")
        old_password = st.text_input("Old Password", type='password')
        new_password = st.text_input("New Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        if st.button("Reset Password"):
            if new_password != confirm_password:
                st.error("New passwords do not match")
                return
            cursor = self.db.cursor()
            query = "UPDATE users SET password = %s WHERE username = %s AND password = %s"
            try:
                cursor.execute(query, (new_password, username, old_password))
                self.db.commit()
                st.success("Password reset successful")
            except:
                st.error("Password reset failed")
    
    def run(self):
        auth.login_page(self.login)
        auth.register_page(self.register)
        auth.reset_password_page(self.reset_password)
        auth.logout_page()
        with auth.authenticated_session():
            st.set_page_config(**self.config)
            # Your existing Streamlit code goes here

app = MyDashboard()
app.run()
