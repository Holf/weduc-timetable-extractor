from weduc_timetable_extractor._config_management import (
    get_chromium_path,
    validate_chromium_path,
)

from ._login_to_weduc import _login_to_weduc


def launch_browser_and_log_in(weduc_credentials, use_headless, p):
    print("Launching browser ...")

    chromium_path = get_chromium_path()
    validate_chromium_path(chromium_path)
    print("Using browser located at:", chromium_path)

    browser = p.chromium.launch(executable_path=chromium_path, headless=use_headless)
    page = browser.new_page()

    page.goto("https://app.weduc.co.uk/")
    _login_to_weduc(page, weduc_credentials)

    return page
