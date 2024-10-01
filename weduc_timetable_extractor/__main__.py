from playwright.sync_api import sync_playwright

from weduc_timetable_extractor import get_command_line_args
from weduc_timetable_extractor.config_management import (
    get_student_configs,
    get_weduc_credentials,
)
from weduc_timetable_extractor.google_calendar_management import (
    push_timetable_to_google_calendar,
)
from weduc_timetable_extractor.icalendar_management import write_timetable_to_ics_file
from weduc_timetable_extractor.weduc_interaction import (
    extract_schools_data_from_weduc,
    extract_timetable_from_weduc_and_add_to_student_config,
    launch_browser_and_log_in,
)


def main():
    args = get_command_line_args()
    weduc_credentials = get_weduc_credentials()
    use_headless = weduc_credentials["credentials_present"]

    student_configs = get_student_configs()
    student_config_count = len(student_configs)
    print(f"Found {student_config_count} student config(s)")

    with sync_playwright() as p:
        print(
            "All login credentials are present in config, so using a headless browser to extract data from Weduc."
            if use_headless
            else "A complete set of login credentials is not present in config, so using a headed browser to allow manual entry."
        )

        page = launch_browser_and_log_in(weduc_credentials, use_headless, p)

        schools = extract_schools_data_from_weduc(page)

        for student_config in student_configs:
            add_summary_info_to_student_config(student_config)
            extract_timetable_from_weduc_and_add_to_student_config(
                page, schools, student_config
            )

    for student_config in student_configs:

        match args.mode:
            case "ical":
                write_timetable_to_ics_file(student_config)

            case "api":
                push_timetable_to_google_calendar(student_config)


def add_summary_info_to_student_config(student_config):
    student_config[
        "info_summary"
    ] = f"""    {student_config["student_name"]}
at school:
    {student_config["school_name"]}
"""


if __name__ == "__main__":
    main()
