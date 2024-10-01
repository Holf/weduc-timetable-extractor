from ._extract_students_data_from_weduc import _extract_students_data_from_weduc
from ._extract_timetable_from_weduc import _extract_timetable_from_weduc
from ._filter_and_transform_timetable import _filter_and_transform_timetable
from ._set_active_school_in_weduc import _set_active_school_in_weduc


def extract_timetable_from_weduc_and_add_to_student_config(
    page, schools, student_config
):
    print("\nExtracting timetable for student:")
    print(student_config["info_summary"])

    _add_school_id_to_student_config(student_config, schools)
    _set_active_school_in_weduc(page, student_config)

    students = _extract_students_data_from_weduc(page)
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
    student_config["timetable"] = _filter_and_transform_timetable(
        _extract_timetable_from_weduc(page, student_config)
    )
