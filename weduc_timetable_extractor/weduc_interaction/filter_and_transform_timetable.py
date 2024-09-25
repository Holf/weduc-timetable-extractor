from datetime import datetime, timezone


def filter_and_transform_timetable(timetable):
    today_utc = datetime.now(timezone.utc)

    print("Transforming timetable and removing past events ...")

    return [
        {
            **event,
            **(
                popover := {
                    key: value
                    for key, value in (
                        entry.split(": ", 1) for entry in event["popover"]
                    )
                }
            ),
            "description": "\n".join(event["popover"]),
            "summary": f'{popover.get("Subject name", "")} - {popover.get("Room name", "")} ({event.get("title", "")})',
        }
        for event in timetable
        if datetime.fromisoformat(event["start"]) >= today_utc
    ]
