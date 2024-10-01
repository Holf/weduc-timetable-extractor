import sys

from googleapiclient.errors import HttpError


def get_google_calendar_id(service, calendar_name):

    try:

        calendars = service.calendarList().list().execute()

        calendarOfInterest = next(
            (c for c in calendars["items"] if c["summary"] == calendar_name),
            None,
        )

        calendarId = calendarOfInterest["id"]

        return calendarId

    except HttpError as error:
        print(f"An error occurred: {error}")
        sys.exit("\nUnable to get Google Calendar Id\n")
