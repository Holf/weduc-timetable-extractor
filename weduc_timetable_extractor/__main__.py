from playwright.sync_api import sync_playwright

from .extract_timetable_from_weduc import extract_timetable_from_weduc
from .filter_and_transform_timetable import filter_and_transform_timetable
from .get_command_line_args import get_command_line_args
from .get_config import get_student_configs, get_weduc_credentials
from .login import login
from .push_timetable_to_google_calendar import push_timetable_to_google_calendar
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

        login(page, weduc_credentials)

        for student_config in student_configs:
            student_config["timetable"] = filter_and_transform_timetable(
                extract_timetable_from_weduc(page, student_config)
            )

            match args.mode:
                case "ical":
                    write_timetable_to_ics_file(args.output_folder_path, student_config)

                case "api":
                    push_timetable_to_google_calendar(student_config)


if __name__ == "__main__":
    main()
