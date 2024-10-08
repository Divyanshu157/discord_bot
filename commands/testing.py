import requests
import base64
import os

# Replace these with your actual Client ID and Secret
client_id = os.getenv("ZOOM_CLIENT_ID")  
client_secret = os.getenv("ZOOM_CLIENT_SECRET")  

# Create the Basic Auth token
credentials = f"{'B5qX__iJStmVRYhZFHLA6A'}:{'A89sbBbEYEm8qjyP4sy76qQ86624HG7w'}"
basic_auth_token = base64.b64encode(credentials.encode()).decode()

def get_access_token():
    url = "https://zoom.us/oauth/token"
    headers = {
        'Authorization': f'Basic {basic_auth_token}',
        'Content-Type': 'application/x-www-form-urlencoded',  # Important
    }
    data = {
        'grant_type': 'client_credentials',
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error obtaining access token: {response.json()}")
        return None

# Get the access token
# access_token = get_access_token()
# if access_token:
#     print("Access Token:latest ", access_token)
# else:
#     print("Failed to obtain access token.")
