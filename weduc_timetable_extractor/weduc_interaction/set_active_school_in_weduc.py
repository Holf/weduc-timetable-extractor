from playwright.sync_api import Page


def set_active_school_in_weduc(page: Page, student_config):

    school_id, school_name = (
        student_config["school_id"],
        student_config["school_name"],
    )

    print(f"Setting active school to '{school_name}' in Weduc ...")

    page.evaluate(
        """
    async (school_id) => {
        async function setActiveSchool() {
            await fetch('https://app.weduc.co.uk/dashboard/index/setcurrent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'entity': school_id
                })
            });
        }
        await setActiveSchool();
    }
    """,
        school_id,
    )

    print("School activated ...")
