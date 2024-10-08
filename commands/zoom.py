import requests
import datetime
import os
import base64
from commands.add_to_calender import add_to_google_calendar

# Set your Client ID and Secret
CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")  # Replace with your Zoom Client ID
CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")  # Replace with your Zoom Client Secret

# Function to get an access token
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
basic_auth_token = base64.b64encode(credentials.encode()).decode()

def get_access_token():
    url = "https://zoom.us/oauth/token"
    # url = "https://zoom.us/oauth/token?grant_type=client_credentials"
    headers = {
        'Authorization': f'Basic {basic_auth_token}',
        'Content-Type': 'application/x-www-form-urlencoded',  # Important
    }
    data = {
        'grant_type': 'account_credentials',
        "account_id": os.getenv("ACCOUNT_ID")
    }
    

    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("Done with Auth")
        print(response)
        return response.json()['access_token']
    else:
        print(f"Error obtaining access token: {response.json()}")
        return None

# Function to create a Zoom meeting
def create_zoom_meeting(participants, meeting_time):
    access_token =get_access_token()
    print("Access Token latest: ", access_token)  # Print to verify

    
    meeting_details = {
    "topic":"testing 01",
    "type":"2",
    "duration":"60",
    "timezone":"America/Mexico",
    "password":"123",
    "agenda":"testing  for generating link",
    "setting":{
        "host_video":"true",
        "participants":"true",
        "join_before_host":"true",
        "mute_upon_entry":"true",
        "break_room":{
            "enable":"true"
        }

    }
}

    headers = {
        
        'Content-Type': 'application/json',
        "Authorization": f'Bearer {access_token}',
    }

    response = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        headers=headers,
        json=meeting_details
    )
    print(response)

    if response.status_code == 201:
        meeting_info = response.json()
        # zoom_link = meeting_info['join_url']

        # # Call the external add_to_google_calendar function
        # add_to_google_calendar.delay(participants, meeting_time, zoom_link, "Zoom Meeting")
        return meeting_info['join_url']  # Return the Zoom meeting link
    else:
        print(f"Error creating meeting: {response.json()}")
        return None

# Example usage
participants = ['participant1@example.com', 'participant2@example.com']
meeting_time = '2024-09-23T10:00:00Z'  # UTC format
zoom_link = create_zoom_meeting(participants, meeting_time)
print("Zoom meeting link:", zoom_link)