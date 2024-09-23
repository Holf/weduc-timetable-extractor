from googleapiclient.errors import HttpError

from .convert_transformed_timetable_to_google_calendar_events import (
    convert_transformed_timetable_to_google_calendar_events,
)
from .get_google_calendar_id import get_google_calendar_id
from .get_google_calendar_service import get_google_calendar_service


def get_event_exists(service, calendar_id, event_id):
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        return event is not None
    except:
        return None


def push_timetable_to_google_calendar(student_config):

    timetable, calendar_name = (
        student_config["timetable"],
        student_config["calendar_to_update"],
    )

    print(f"Pushing events to Google Calendar '{calendar_name}' via API")

    print("Converting timetable to Google Calendar events ...")
    google_calendar_events = convert_transformed_timetable_to_google_calendar_events(
        timetable
    )

    service = get_google_calendar_service()

    try:
        calendar_id = get_google_calendar_id(service, calendar_name)

        # Prints the start and name of the next 10 events
        for event in google_calendar_events:
            event_id = event["id"]

            print(f"Processing event with id: {event_id}")

            if get_event_exists(service, calendar_id, event_id):
                print(f"    Updating existing event ... ", end="")

                service.events().update(
                    calendarId=calendar_id, eventId=event_id, body=event
                ).execute()

                print("event updated")

            else:
                print("    Inserting new event ... ", end="")

                service.events().insert(calendarId=calendar_id, body=event).execute()

                print("event inserted")

        print(
            f"Pushed a total of {len(google_calendar_events)} events to Google Calender"
        )
        print()

    except HttpError as error:
        print(f"An error occurred: {error}")
