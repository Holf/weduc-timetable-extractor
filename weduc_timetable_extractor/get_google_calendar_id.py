from googleapiclient.errors import HttpError

from .get_config import get_config
from .throw_error import throw_error


def get_google_calendar_id(service):

    try:

        calendars = service.calendarList().list().execute()

        calendar_name = get_config("google_calendar", "calendar_to_update")

        calendarOfInterest = next(
            (c for c in calendars["items"] if c["summary"] == calendar_name),
            None,
        )

        calendarId = calendarOfInterest["id"]

        return calendarId

    except HttpError as error:
        print(f"An error occurred: {error}")
        throw_error("Unable to get Google Calendar Id")
