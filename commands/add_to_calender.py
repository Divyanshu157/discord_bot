# add_to_calendar.py

import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from commands.celery_config import celery_app

# Function to authenticate Google Calendar API
def authenticate_google_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('commands/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Function to add a meeting to Google Calendar
# @celery_app.task
def add_to_google_calendar(participants, meeting_time, meeting_link, meeting_topic="Meeting"):
    # Authenticate Google Calendar API
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    # Define start and end times
    start_time = meeting_time
    end_time = (datetime.datetime.fromisoformat(meeting_time) + datetime.timedelta(hours=1)).isoformat()

    # Create the calendar event
    event = {
        'summary': meeting_topic,
        'description': f'Join the meeting: {meeting_link}',  # Add meeting link to description
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Mexico_City',
        },
        'attendees': [{'email': email} for email in participants],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # Insert the event into the primary calendar
    event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print(f"Event created in Google Calendar: {event['htmlLink']}")
    return event['htmlLink']
