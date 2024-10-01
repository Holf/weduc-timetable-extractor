import os
import sys
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
    creds = None

    if getattr(sys, "frozen", False):
        # We are running in a bundle (PyInstaller)
        project_root = Path(sys.executable).resolve().parent
    else:
        # We are running in a normal Python environment
        project_root = Path(__file__).resolve().parent.parent.parent

    token_file_path = project_root / "token.json"
    credentials_file_path = project_root / "credentials.json"
    validate_credentials_path(credentials_file_path)

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


def validate_credentials_path(credentials_file_path):
    if not credentials_file_path.is_file():
        sys.exit(
            f"""Error: there is no Google Calendar API 'credentials.json' file present in the same folder as the executable.
See the project documentation for info on setting this up: https://github.com/Holf/weduc-timetable-extractor/blob/main/README.md"""
        )
