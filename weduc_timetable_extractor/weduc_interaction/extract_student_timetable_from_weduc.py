from .extract_students_data_from_weduc import extract_students_data_from_weduc
from .extract_timetable_from_weduc import extract_timetable_from_weduc
from .filter_and_transform_timetable import filter_and_transform_timetable
from .set_active_school_in_weduc import set_active_school_in_weduc


def extract_student_timetable_from_weduc(page, schools, student_config):
    print("\nExtracting timetable for student:")
    print(student_config["info_summary"])

    _add_school_id_to_student_config(student_config, schools)
    set_active_school_in_weduc(page, student_config)

    students = extract_students_data_from_weduc(page)
    _add_student_id_to_student_config(student_config, students)

    _extract_timetable_and_add_to_student_config(page, student_config)


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
