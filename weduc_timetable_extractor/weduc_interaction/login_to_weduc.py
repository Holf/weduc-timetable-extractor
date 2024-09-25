from playwright.sync_api import Page

from ..constants import WEDUC_LOGIN_TIMEOUT


def login_to_weduc(page: Page, weduc_credentials):

    print("Logging in to Weduc ...")

    if username := weduc_credentials["username"]:
        username_input = page.get_by_label("Login or E-mail")
        username_input.wait_for()
        username_input.type(username)

    if password := weduc_credentials["password"]:
        password_input = page.get_by_label("Password")
        password_input.wait_for()
        password_input.type(password)

    if weduc_credentials["credentials_present"]:
        login_button = page.get_by_role("button", name="Login")
        login_button.click()

    page.wait_for_function(
        "localStorage.getItem('wfx_unq') !== null", timeout=WEDUC_LOGIN_TIMEOUT
    )

    page.wait_for_function(
        "localStorage.getItem('wfx_UUID') !== null", timeout=WEDUC_LOGIN_TIMEOUT
    )
