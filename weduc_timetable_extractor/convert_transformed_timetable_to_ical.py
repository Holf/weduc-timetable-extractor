from datetime import datetime

from icalendar import Calendar, Event


def convert_transformed_timetable_to_ical(transformed_timetable):

    cal = Calendar()

    for event in transformed_timetable:
        ical_event = Event()
        ical_event.add("summary", event["summary"])
        ical_event.add("dtstart", datetime.fromisoformat(event["start"]))
        ical_event.add("dtend", datetime.fromisoformat(event["end"]))
        ical_event.add("uid", str(event["id"]))
        ical_event.add("description", event["description"])

        cal.add_component(ical_event)

    ical_content = cal.to_ical().decode("utf-8")

    return ical_content
