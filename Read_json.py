import requests
import json

def send_post_request(url, json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("POST request successful!")
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print(response.text)

    except FileNotFoundError:
        print("Error: JSON file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'your_url_here' with the actual URL where you want to send the POST request
    url = 'your_url_here'
    json_file_path = 'data.json'

    send_post_request(url, json_file_path)
                  
