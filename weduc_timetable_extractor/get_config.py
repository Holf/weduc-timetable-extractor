import configparser
from pathlib import Path

config = None


def get_config(section, option):

    global config

    if config == None:
        project_root = Path(__file__).resolve().parent.parent
        config_file_path = project_root / "config.ini"

        config = configparser.ConfigParser()
        config.read(config_file_path)

    if not config.has_option(section, option):
        return None

    return config.get(section, option)
