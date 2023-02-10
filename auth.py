
# get_access_token: This function makes a POST request to the token endpoint
# with the authorization code, client ID, client secret, and redirect URL
# to get the access token.

# get_user_info: This function makes a GET request to the authorization
# endpoint with the access token to get the user information.

# check_group_membership: This function checks if the user is a member of the specified
# group by checking if the group is present in the list of groups returned in the user
# information.

# authenticate: This function calls the get_access_token and get_user_info functions
# and then checks if the user is a member of the specified group.


import requests
# OAuth2 configuration parameters
redirect_url = "http://localhost:8000/callback"
client_id = "your_client_id"
client_secret = "your_client_secret"
authorization_endpoint = "https://your_authorization_endpoint"
token_endpoint = "https://your_token_endpoint"


def get_access_token(code):

    # Request access token from the token endpoint
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_url,
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_endpoint, data=data, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print("Error while fetching access token:", e)
        return None


def get_user_info(access_token):

    # Request user information from the authorization endpoint
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(authorization_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error while fetching user information:", e)
        return None


def check_group_membership(user_info, group):

    # Check if the user is a member of the specified group
    groups = user_info.get("groups", [])
    return group in groups


def authenticate(code, group):
    # Authenticate the user by first getting the access token and then the user information
    access_token = get_access_token(code)
    if not access_token:
        return False
    user_info = get_user_info(access_token)
    if not user_info:
        return False
    return check_group_membership(user_info, group)
