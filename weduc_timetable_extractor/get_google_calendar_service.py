import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_calendar_service():
    creds = get_credentials()

    service = build("calendar", "v3", credentials=creds)

    return service


def get_credentials():
    """Shows basic usage of the Google Calendar API."""
    creds = None

    project_root = Path(__file__).resolve().parent.parent
    token_file_path = project_root / "token.json"
    credentials_file_path = project_root / "credentials.json"

    # Check if token.json exists, which stores the user's access and refresh tokens.
    if os.path.exists(token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
    # If there are no valid credentials, log the user in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use.
        with open(token_file_path, "w") as token:
            token.write(creds.to_json())
    return creds
