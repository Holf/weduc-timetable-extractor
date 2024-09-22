from datetime import datetime, timezone

from googleapiclient.errors import HttpError

from .convert_transformed_timetable_to_google_calendar_events import (
    convert_transformed_timetable_to_google_calendar_events,
)
from .get_config import get_config
from .get_google_calendar_id import get_google_calendar_id
from .get_google_calendar_service import get_google_calendar_service


def get_event_exists(service, calendar_id, event_id):
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        return event is not None
    except:
        return None


def push_timetable_to_google_calendar(timetable):

    google_calendar_events = convert_transformed_timetable_to_google_calendar_events(
        timetable
    )

    service = get_google_calendar_service()

    try:
        calendar_id = get_google_calendar_id(service)

        # Prints the start and name of the next 10 events
        for event in google_calendar_events:
            event_id = event["id"]

            print(f"Processing event with id: {event_id}")

            if get_event_exists(service, calendar_id, event_id):

                print(f"Updating existing event with ID: {event_id} ...")

                service.events().update(
                    calendarId=calendar_id, eventId=event_id, body=event
                ).execute()

                print("Event updated")

            else:

                print("Inserting new event ...")

                service.events().insert(calendarId=calendar_id, body=event).execute()

                print("Event inserted")

    except HttpError as error:
        print(f"An error occurred: {error}")
