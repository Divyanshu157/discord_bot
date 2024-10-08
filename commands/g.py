import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# Set the Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Function to authenticate using credentials.json
def authenticate_google_calendar():
    creds = None
    # Token.json stores the user's access and refresh tokens and is created automatically when the authorization flow completes.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the credentials.json file here for authentication
            flow = InstalledAppFlow.from_client_secrets_file('commands/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Function to create a Google Meet meeting
def create_google_meet(participants, meeting_time, meeting_topic="Google Meet Meeting"):
    # Authenticate the Google Calendar API
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    # Create a new event with a Google Meet link
    start_time = meeting_time
    end_time = (datetime.datetime.fromisoformat(meeting_time) + datetime.timedelta(hours=1)).isoformat()

    event = {
        'summary': meeting_topic,
        'description': 'Google Meet for testing',
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Mexico_City',
        },
        'attendees': [{'email': email} for email in participants],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet',
                },
                'requestId': 'random-string-1234',
            },
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # Insert the event in the primary calendar with Google Meet link
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    meet_link = event['hangoutLink']
    print(f"Google Meet Link: {meet_link}")
    return meet_link

# Example usage
participants = ['participant1@example.com', 'participant2@example.com']
meeting_time = '2024-09-23T10:00:00'  # UTC format
google_meet_link = create_google_meet(participants, meeting_time)
print("Google Meet link:", google_meet_link)
