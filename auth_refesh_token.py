# In this modified code, we first check if the access token and its expiration
# time are present in the session state. If the token has not expired,
# we use it to make an API call. If the token has expired, we use the refresh
# token to obtain a new access token.

# If the token refresh is successful, we update the session state with the new access token,
# refresh token, and expiration time. If the refresh fails, we prompt the user to login again.

# Note that this is just an example and you should modify it to suit your specific use case.


import requests

import streamlit as st


# Define variables

client_id = '<your-client-id>'

client_secret = '<your-client-secret>'

redirect_uri = '<your-redirect-uri>'

oauth_authorization_endpoint = '<your-authorization-endpoint>'

oauth_token_endpoint = '<your-token-endpoint>'

userinfo_endpoint = '<your-userinfo-endpoint>'


# Check if access token exists and is not expired

if 'access_token' in st.session_state and 'expires_at' in st.session_state:

    if st.session_state['expires_at'] > time.time():

        access_token = st.session_state['access_token']

    else:

        # Access token has expired, refresh it

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {

            'grant_type': 'refresh_token',

            'refresh_token': st.session_state['refresh_token'],

            'client_id': client_id,

            'client_secret': client_secret

        }

        response = requests.post(oauth_token_endpoint,
                                 headers=headers, data=data)

        if response.status_code == 200:

            # Token refreshed successfully

            token_data = response.json()

            st.session_state['access_token'] = token_data['access_token']

            st.session_state['refresh_token'] = token_data['refresh_token']

            st.session_state['expires_at'] = time.time() + \
                token_data['expires_in']

            access_token = token_data['access_token']

        else:

            # Token refresh failed, prompt user to login again

            st.write("Token refresh failed, please login again")

            st.button("Login")


else:

    # Access token does not exist, prompt user to login

    st.write("Please login to continue")

    st.button("Login")
