from playwright.sync_api import Page


def _extract_students_data_from_weduc(page: Page):

    print("Extracting student ID info from Weduc ...")

    weduc_config = get_weduc_config(page)
    students = weduc_config["Body"]["auth"]["props"]["children"]

    return students


def get_weduc_config(page):
    return page.evaluate(
        """
    async () => {
        async function fetchData() {            
            const response = await fetch(`https://app.weduc.co.uk/dashboard/newsfeed/config`);
            return await response.json();
        }
        return await fetchData();
    }
    """,
    )
