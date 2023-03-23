import requests
import json
import datetime

# Define the PI Web API endpoint and authentication details
base_url = 'https://your-pi-web-api-url.com/piwebapi'
username = 'your-username'
password = 'your-password'

# Define the tag name and the value to write to it
tag_name = 'sinusoid'
tag_value = 3.14

# Create a timestamp for the value
timestamp = datetime.datetime.utcnow().isoformat() + 'Z'

# Build the JSON payload for the write request
payload = json.dumps([{"Timestamp": timestamp, "Value": tag_value}])

# Define the headers for the request, including the authentication token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
auth_token = requests.post(base_url + '/identity/token', auth=(username, password)).json()['access_token']
headers['Authorization'] = 'Bearer ' + auth_token

# Build the URL for the write request and send the request
write_url = f"{base_url}/streams/{tag_name}/value"
response = requests.post(write_url, headers=headers, data=payload)

# Check if the write was successful
if response.ok:
    print('Value written successfully!')
else:
    print(f'Error writing value: {response.text}')
