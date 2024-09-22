from playwright.sync_api import sync_playwright

from .convert_transformed_timetable_to_ical import convert_transformed_timetable_to_ical
from .extract_timetable_from_weduc import extract_timetable_from_weduc
from .filter_and_transform_timetable import filter_and_transform_timetable
from .get_command_line_args import get_command_line_args
from .push_timetable_to_google_calendar import push_timetable_to_google_calendar


def main():
    args = get_command_line_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://app.weduc.co.uk/")

        timetable = extract_timetable_from_weduc(page)
        print(f"Extracted {len(timetable)} events from WeDuc ...")

    timetable = filter_and_transform_timetable(timetable)
    print(f"Found {len(timetable)} events from today onwards ...")

    match args.mode:
        case "ical":
            print(f"Writing events as iCalendar format to file: {args.output_path}")
            write_ics_file(args.output_path, timetable)

        case "api":
            print(f"Pushing events to Google Calendar via API")
            push_timetable_to_google_calendar(timetable)


def write_ics_file(output_path, timetable):
    ical_content = convert_transformed_timetable_to_ical(timetable)

    with open(output_path, "w") as file:
        file.write(ical_content)


if __name__ == "__main__":
    main()
