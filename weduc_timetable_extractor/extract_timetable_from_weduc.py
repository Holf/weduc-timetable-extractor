import sys

from playwright.sync_api import Page

from .get_config import get_config

login_timeout = 5 * 60 * 1000  # 5 minutes


def check_config(key):
    if not (value := get_config("weduc", key)):
        sys.stderr.write(f"\nError: There is no 'weduc.{key}' present in config.ini")
        sys.exit(2)
    return value


def login(page: Page):

    if username := get_config("weduc", "username"):
        username_input = page.get_by_label("Login or E-mail")
        username_input.wait_for()
        username_input.type(username)

    if password := get_config("weduc", "password"):
        password_input = page.get_by_label("Password")
        password_input.wait_for()
        password_input.type(password)

    if username != "" and password != "":
        login_button = page.get_by_role("button", name="Login")
        login_button.click()


def extract_timetable_from_weduc(page: Page):

    school_id = check_config("school_id")
    student_id = check_config("student_id")

    login(page)

    page.wait_for_function(
        "localStorage.getItem('wfx_unq') !== null", timeout=login_timeout
    )

    page.wait_for_function(
        "localStorage.getItem('wfx_UUID') !== null", timeout=login_timeout
    )

    response_data = page.evaluate(
        """
    async ({school_id, student_id}) => {
        async function fetchData() {
            await fetch('https://app.weduc.co.uk/dashboard/index/setcurrent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'entity': school_id
                })
            });
            
            const response = await fetch(`https://app.weduc.co.uk/user/profile/getTimetable/user/${student_id}/`);
            return await response.json();
        }
        return fetchData();
    }
    """,
        {"school_id": school_id, "student_id": student_id},
    )

    timetable = response_data["Body"]["timetable"]

    return timetable
