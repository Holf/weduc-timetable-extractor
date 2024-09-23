from playwright.sync_api import Page


def extract_timetable_from_weduc(page: Page, student_config):

    section_name, school_id, student_id = (
        student_config["section_name"],
        student_config["school_id"],
        student_config["student_id"],
    )

    print(f"Extracting timetable for: '{section_name}' ...")

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
