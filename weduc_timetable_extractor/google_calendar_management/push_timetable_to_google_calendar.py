from googleapiclient.errors import HttpError

from ._convert_transformed_timetable_to_google_calendar_events import (
    _convert_transformed_timetable_to_google_calendar_events,
)
from ._get_google_calendar_id import _get_google_calendar_id
from ._get_google_calendar_service import _get_google_calendar_service


def push_timetable_to_google_calendar(student_config):
    print("\nPushing timetable events to Google Calendar for student:")
    print(student_config["info_summary"])

    timetable, calendar_name = (
        student_config["timetable"],
        student_config["calendar_to_update"],
    )

    google_calendar_events = _convert_transformed_timetable_to_google_calendar_events(
        timetable
    )

    print(f'Pushing events to Google Calendar "{calendar_name}" ... ')
    print(
        """I: signifies an inserted event
U: signifies an updated event"""
    )

    service = _get_google_calendar_service()

    try:
        calendar_id = _get_google_calendar_id(service, calendar_name)

        for event in google_calendar_events:
            event_id = event["id"]

            if get_event_exists(service, calendar_id, event_id):

                service.events().update(
                    calendarId=calendar_id, eventId=event_id, body=event
                ).execute()

                print("U", end="", flush=True)

            else:

                service.events().insert(calendarId=calendar_id, body=event).execute()

                print("I", end="", flush=True)

        print(
            f"\nPushed a total of {len(google_calendar_events)} events to Google Calender"
        )
        print()

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_event_exists(service, calendar_id, event_id):
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        return event is not None
    except:
        return None
