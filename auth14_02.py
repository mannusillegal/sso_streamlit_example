import requests
import streamlit as st

def get_access_token(redirect_url, client_id, client_secret, oauth_token_endpoint):
    data = {
        "grant_type": "authorization_code",
        "redirect_uri": redirect_url,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(oauth_token_endpoint, data=data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception("Failed to get access token")

def authenticate_user(access_token, user_info_endpoint):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(user_info_endpoint, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        raise Exception("Failed to authenticate user")

def validate_user(user_info, required_roles):
    user_roles = user_info.get("roles")
    if not set(required_roles).issubset(set(user_roles)):
        raise Exception("User does not have required roles")

def main(redirect_url, client_id, client_secret, oauth_authorization_endpoint, oauth_token_endpoint, user_info_endpoint):
    try:
        access_token = get_access_token(redirect_url, client_id, client_secret, oauth_token_endpoint)
        user_info = authenticate_user(access_token, user_info_endpoint)
        required_roles = ["admin", "user"]
        validate_user(user_info, required_roles)

        st.write("Login Successful!")
        st.write("Access Token: ", access_token)
        st.write("User Info: ", user_info)
        
        # Streamlit code goes here
        st.header("Streamlit Dashboard")
        st.write("Welcome to the Streamlit Dashboard!")
    except Exception as e:
        st.write("Error: ", str(e))

if __name__ == "__main__":
    redirect_url = "http://localhost:8501"
    client_id = "your-client-id"
    client_secret = "your-client-secret"
    oauth_authorization_endpoint = "https://oauth.example.com/authorize"
    oauth_token_endpoint = "https://oauth.example.com/token"
    user_info_endpoint = "https://oauth.example.com/userinfo"

    main(redirect_url, client_id, client_secret, oauth_authorization_endpoint, oauth_token_endpoint, user_info_endpoint)
