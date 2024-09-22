import argparse

from .get_config import get_config
from .throw_error import throw_error


def get_command_line_args():
    parser = argparse.ArgumentParser(
        prog="Weduc Timetable Extractor",
        description="Extracts timetable information from Weduc and either: exports it as an iCalendar file; or, uses Google Calendar API to push it to a Google Calendar",
    )

    subparsers = parser.add_subparsers(
        help="Choose 'ical' or 'api'", dest="mode", required=True
    )

    parser_ical = subparsers.add_parser(
        "ical",
        help="Generate an iCalendar '.ics' file from the extracted Weduc timetable",
    )
    parser_ical.add_argument(
        "output_path", help="The output path for the generated '.ics' file"
    )

    subparsers.add_parser(
        "api", help="Push the extracted Weduc timetable to Google Calendar"
    )

    args = parser.parse_args()

    if args.mode == "api":
        config = get_config("google_calendar", "calendar_to_update")

        if config == None:
            throw_error(
                "Error: mode of 'api' was specified but there is no 'google_calendar.calendar_to_update' present in config.ini"
            )

    return args
