import configparser
import platform
import sys
from pathlib import Path

from ._constants import STUDENT_SECTION_NAME_PREFIX, WEDUC_SECTION_NAME

config = None


def get_config():

    global config

    if config == None:
        if getattr(sys, "frozen", False):
            # We are running in a bundle (PyInstaller)
            project_root = Path(sys.executable).resolve().parent
        else:
            # We are running in a normal Python environment
            project_root = Path(__file__).resolve().parent.parent

        config_file_path = project_root / "config.ini"
        validate_config_ini_path(config_file_path)

        config = configparser.ConfigParser()
        config.read(config_file_path)

    return config


def get_config_option(section, option, throw_if_absent=False):
    config = get_config()

    # Check if the option exists
    if not config.has_option(section, option):
        value = None
    else:
        value = config.get(section, option).strip() or None

    # Handle the absence of value if throw_if_absent is True
    if value is None and throw_if_absent:
        sys.exit(f"\nError: There is no '{section}.{option}' present in config.ini")

    return value


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


def get_ics_folder_path(throw_if_absent=False):
    return get_config_option("ical", "output_folder_path", throw_if_absent)


def get_chromium_path():
    chromium_path = get_config_option(WEDUC_SECTION_NAME, "chromium_path")

    if chromium_path != None:
        return chromium_path

    os_map = {
        "Windows": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "Linux": "/usr/bin/google-chrome",
        "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    }

    return os_map.get(platform.system())


def validate_config_ini_path(config_ini_file_path):
    if not config_ini_file_path.is_file():
        sys.exit(
            f"Error: unable to find a config.ini file at path '{config_ini_file_path}'"
        )


def validate_chromium_path(chromium_path):
    if not Path(chromium_path).is_file():
        sys.exit(f"Error: unable to find a browser at path '{chromium_path}'")


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

    validate_at_least_one_student_config(student_configs)

    return student_configs


def validate_at_least_one_student_config(student_configs):
    student_config_count = len(student_configs)

    if student_config_count > 0:
        return student_config_count

    sys.exit("Error: there are no student configs in config.ini")


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
