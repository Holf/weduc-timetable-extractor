from playwright.sync_api import Page


def extract_schools_data_from_weduc(page: Page):

    school_links = page.locator("a[data-id]")

    schools_data = [
        {
            "school_id": link.get_attribute("data-id"),
            "school_name": link.text_content().strip(),
        }
        for link in school_links.element_handles()
    ]

    return schools_data
