from playwright.sync_api import Page


def extract_timetable_from_weduc(page: Page, student_config):

    student_id = student_config["student_id"]

    print("Extracting timetable from Weduc ...")

    response_data = page.evaluate(
        """
    async (student_id) => {
        async function fetchData() {
            const response = await fetch(`https://app.weduc.co.uk/user/profile/getTimetable/user/${student_id}/`);
            return await response.json();
        }
        return await fetchData();
    }
    """,
        student_id,
    )

    timetable = response_data["Body"]["timetable"]

    return timetable
