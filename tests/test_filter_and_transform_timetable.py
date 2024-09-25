import json

from weduc_timetable_extractor.weduc_interaction import filter_and_transform_timetable


def test_filter_and_transform_timetable(snapshot):

    with open("./tests/assets/weduc_response.json", "r") as file:
        timetable = json.load(file)["Body"]["timetable"]

    result = filter_and_transform_timetable(timetable)

    assert snapshot == result
