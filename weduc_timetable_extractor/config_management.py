import configparser
import sys
from pathlib import Path

from .constants import STUDENT_SECTION_NAME_PREFIX, WEDUC_SECTION_NAME

config = None


def get_config():

    global config

    if config == None:
        project_root = Path(__file__).resolve().parent.parent
        config_file_path = project_root / "config.ini"

        config = configparser.ConfigParser()
        config.read(config_file_path)

    return config


def get_config_option(section, option, throw_if_absent=False):
    config = get_config()

    if not config.has_option(section, option):
        if throw_if_absent:
            sys.stderr.write(
                f"\nError: There is no '{section}.{option}' present in config.ini"
            )
            sys.exit(2)
        else:
            return None

    return config.get(section, option)


def get_weduc_credentials():

    username, password = get_config_option(
        WEDUC_SECTION_NAME, "username"
    ), get_config_option(WEDUC_SECTION_NAME, "password")

    credentials = {
        "username": username,
        "password": password,
        "credentials_present": username != None and password != None,
    }

    return credentials


def get_chromium_path():
    return get_config_option(WEDUC_SECTION_NAME, "chromium_path")


def get_student_configs():
    section_names = get_config().sections()
    student_section_names = [
        section_name.lower()
        for section_name in section_names
        if section_name.startswith(STUDENT_SECTION_NAME_PREFIX)
    ]

    student_configs = [
        get_student_config(section_name) for section_name in student_section_names
    ]

    return student_configs


def get_student_config(section_name):
    return {
        "section_name": section_name,
        "school_name": get_config_option(
            section_name, "school_name", throw_if_absent=True
        ),
        "student_name": get_config_option(
            section_name, "student_name", throw_if_absent=True
        ),
        "calendar_to_update": get_config_option(section_name, "calendar_to_update"),
    }
