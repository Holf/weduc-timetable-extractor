from playwright.sync_api import sync_playwright

from weduc_timetable_extractor import get_command_line_args
from weduc_timetable_extractor.config_management import (
    get_chromium_path,
    get_student_configs,
    get_weduc_credentials,
)
from weduc_timetable_extractor.google_calendar_management import (
    push_timetable_to_google_calendar,
)
from weduc_timetable_extractor.icalendar_management import write_timetable_to_ics_file
from weduc_timetable_extractor.weduc_interaction import (
    extract_schools_data_from_weduc,
    extract_students_data_from_weduc,
    extract_timetable_from_weduc,
    filter_and_transform_timetable,
    login_to_weduc,
    set_active_school_in_weduc,
)


def main():
    args = get_command_line_args()
    weduc_credentials = get_weduc_credentials()
    use_headless = weduc_credentials["credentials_present"]

    student_configs = get_student_configs()

    print(f"Found {len(student_configs)} student config(s)")

    with sync_playwright() as p:
        print(
            "All login credentials are present in config, so using a headless browser to extract data from Weduc."
            if use_headless
            else "A complete set of login credentials is not present in config, so using a headed browser to allow manual entry."
        )

        print("Launching browser ...")

        chromium_path = get_chromium_path() or "/usr/bin/google-chrome"
        browser = p.chromium.launch(
            executable_path=chromium_path, headless=use_headless
        )
        page = browser.new_page()

        page.goto("https://app.weduc.co.uk/")

        login_to_weduc(page, weduc_credentials)

        schools = extract_schools_data_from_weduc(page)

        for student_config in student_configs:

            _log_student_info(student_config)

            extract_student_timetable_from_weduc(page, schools, student_config)

            match args.mode:
                case "ical":
                    write_timetable_to_ics_file(args.output_folder_path, student_config)

                case "api":
                    push_timetable_to_google_calendar(student_config)


def extract_student_timetable_from_weduc(page, schools, student_config):
    _add_school_id_to_student_config(student_config, schools)
    set_active_school_in_weduc(page, student_config)

    students = extract_students_data_from_weduc(page, student_config["school_id"])
    _add_student_id_to_student_config(student_config, students)

    _extract_timetable_and_add_to_student_config(page, student_config)


def _log_student_info(student_config):
    print(
        f"""
Processing timetable for student:
    {student_config["student_name"]}
at school:
    {student_config["school_name"]}
"""
    )


def _add_school_id_to_student_config(student_config, schools):

    student_config["school_id"] = next(
        (
            school["school_id"]
            for school in schools
            if school["school_name"] == student_config["school_name"]
        ),
        None,
    )


def _add_student_id_to_student_config(student_config, students):

    student_config["student_id"] = next(
        (
            student["id"]
            for student in students
            if student["name"] == student_config["student_name"]
        ),
        None,
    )


def _extract_timetable_and_add_to_student_config(page, student_config):
    student_config["timetable"] = filter_and_transform_timetable(
        extract_timetable_from_weduc(page, student_config)
    )


if __name__ == "__main__":
    main()
