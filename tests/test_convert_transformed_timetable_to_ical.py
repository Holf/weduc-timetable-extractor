from freezegun import freeze_time

from weduc_timetable_extractor.icalendar_management import (
    _convert_transformed_timetable_to_ical,
)

test_timetable = list(
    [
        dict(
            {
                "Class name": "10w/En1",
                "Room name": "ENGLISH3",
                "Subject name": "English La",
                "Teacher name": "C Reynolds",
                "color": "rgba(255, 107, 00, 0.6)",
                "description": """
        Room name: ENGLISH3
        Class name: 10w/En1
        Subject name: English La
        Teacher name: C Reynolds
      """,
                "end": "2024-09-27T11:20:00+00:00",
                "id": "281475447549934",
                "popover": list(
                    [
                        "Room name: ENGLISH3",
                        "Class name: 10w/En1",
                        "Subject name: English La",
                        "Teacher name: C Reynolds",
                    ]
                ),
                "start": "2024-09-27T10:20:00+00:00",
                "summary": "English La - ENGLISH3 (10w/En1)",
                "title": "10w/En1",
            }
        ),
        dict(
            {
                "Class name": "10B/Dt1",
                "Room name": "DT7",
                "Subject name": "Des.Tech",
                "Teacher name": "S Oti-Akenten",
                "color": "rgba(255, 107, 00, 0.6)",
                "description": """
        Room name: DT7
        Class name: 10B/Dt1
        Subject name: Des.Tech
        Teacher name: S Oti-Akenten
      """,
                "end": "2024-09-27T12:20:00+00:00",
                "id": "281475447549935",
                "popover": list(
                    [
                        "Room name: DT7",
                        "Class name: 10B/Dt1",
                        "Subject name: Des.Tech",
                        "Teacher name: S Oti-Akenten",
                    ]
                ),
                "start": "2024-09-27T11:20:00+00:00",
                "summary": "Des.Tech - DT7 (10B/Dt1)",
                "title": "10B/Dt1",
            }
        ),
        dict(
            {
                "Class name": "10w/Ma2",
                "Room name": "T1",
                "Subject name": "Maths",
                "Teacher name": "V Tucker",
                "color": "rgba(255, 107, 00, 0.6)",
                "description": """
        Room name: T1
        Class name: 10w/Ma2
        Subject name: Maths
        Teacher name: V Tucker
      """,
                "end": "2024-09-27T14:00:00+00:00",
                "id": "281475447549936",
                "popover": list(
                    [
                        "Room name: T1",
                        "Class name: 10w/Ma2",
                        "Subject name: Maths",
                        "Teacher name: V Tucker",
                    ]
                ),
                "start": "2024-09-27T13:00:00+00:00",
                "summary": "Maths - T1 (10w/Ma2)",
                "title": "10w/Ma2",
            }
        ),
    ]
)


@freeze_time("2024-09-15")
def test_convert_json_to_ical(snapshot):

    result = _convert_transformed_timetable_to_ical(test_timetable)

    assert snapshot == result
