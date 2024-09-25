from playwright.sync_api import sync_playwright

from .config_management import get_student_configs, get_weduc_credentials
from .filter_and_transform_timetable import filter_and_transform_timetable
from .get_command_line_args import get_command_line_args
from .push_timetable_to_google_calendar import push_timetable_to_google_calendar
from .weduc_interaction.extract_schools_data_from_weduc import (
    extract_schools_data_from_weduc,
)
from .weduc_interaction.extract_students_data_from_weduc import (
    extract_students_data_from_weduc,
)
from .weduc_interaction.extract_timetable_from_weduc import extract_timetable_from_weduc
from .weduc_interaction.login_to_weduc import login_to_weduc
from .weduc_interaction.set_active_school_in_weduc import set_active_school_in_weduc
from .write_timetable_to_ics_file import write_timetable_to_ics_file


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
        browser = p.chromium.launch(headless=use_headless)
        page = browser.new_page()

        page.goto("https://app.weduc.co.uk/")

        login_to_weduc(page, weduc_credentials)

        schools = extract_schools_data_from_weduc(page)

        for student_config in student_configs:

            _log_student_info(student_config)

            _add_school_id_to_student_config(student_config, schools)

            set_active_school_in_weduc(page, student_config)

            students = extract_students_data_from_weduc(
                page, student_config["school_id"]
            )
            _add_student_id_to_student_config(student_config, students)

            _extract_timetable_and_add_to_student_config(page, student_config)

            match args.mode:
                case "ical":
                    write_timetable_to_ics_file(args.output_folder_path, student_config)

                case "api":
                    push_timetable_to_google_calendar(student_config)


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
