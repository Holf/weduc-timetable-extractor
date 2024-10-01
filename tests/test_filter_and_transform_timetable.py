import json

from freezegun import freeze_time

from weduc_timetable_extractor.weduc_interaction import filter_and_transform_timetable


@freeze_time("2024-09-15")
def test_filter_and_transform_timetable(snapshot):

    with open("./tests/assets/weduc_response.json", "r") as file:
        timetable = json.load(file)["Body"]["timetable"]

    result = filter_and_transform_timetable(timetable)

    assert snapshot == result
