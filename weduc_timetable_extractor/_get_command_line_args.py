import argparse

from ._config_management import get_ics_folder_path


def _get_command_line_args():
    parser = argparse.ArgumentParser(
        prog="Weduc Timetable Extractor",
        description="Extracts timetable information from Weduc and either: exports it as an iCalendar file; or, uses Google Calendar API to push it to a Google Calendar",
    )

    subparsers = parser.add_subparsers(
        help="Choose 'ical' or 'api'", dest="mode", required=True
    )

    subparsers.add_parser(
        "ical",
        help="Generate an iCalendar '.ics' file from the extracted Weduc timetable",
    )

    subparsers.add_parser(
        "api", help="Push the extracted Weduc timetable to Google Calendar"
    )

    args = parser.parse_args()

    if args.mode == "ical":
        print("validaty")
        get_ics_folder_path(throw_if_absent=True)

    return args
