from pathlib import Path

from weduc_timetable_extractor.config_management import get_ics_folder_path

from .convert_transformed_timetable_to_ical import convert_transformed_timetable_to_ical


def write_timetable_to_ics_file(student_config):

    print("\nWriting out iCalendar file for student:")
    print(student_config["info_summary"])

    ics_folder_path = get_ics_folder_path()

    output_folder = Path(ics_folder_path)
    output_folder.mkdir(parents=True, exist_ok=True)

    file_name = student_config["section_name"]
    file_path = (output_folder / file_name).with_suffix(".ics")

    print(f"Writing events as iCalendar format to file: {file_path}")

    ical_content = convert_transformed_timetable_to_ical(student_config["timetable"])
    print("Events converted to iCalendar ...")

    with open(file_path, "w") as file:
        file.write(ical_content)

    print("Events written to file")
