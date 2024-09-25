def convert_transformed_timetable_to_google_calendar_events(transformed_timetable):
    print("Converting timetable to Google Calendar events ...")

    google_calendar_events = []

    for event in transformed_timetable:
        google_calender_event = {
            "id": event["id"],
            "summary": event["summary"],
            "description": event["description"],
            "start": {"dateTime": event["start"]},
            "end": {"dateTime": event["end"]},
        }

        google_calendar_events.append(google_calender_event)

    return google_calendar_events
