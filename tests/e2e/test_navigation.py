"""Readers can reach every part of the site from the home page."""


def heading(page) -> str:
    """The page title, without the ¶ permalink the theme adds to headings."""
    return page.locator("h1").inner_text().rstrip("¶").strip()

import pytest

HOME_CARDS = {
    "Getting started": "Getting started",
    "Tutorials": "Tutorials",
    "User Guide": "User Guide",
    "Developer Guide": "Developer Guide",
}


def test_home_page_loads(page, base_url):
    page.goto(base_url)
    assert page.title().startswith("Home")
    assert heading(page) == "GeoTALOS documentation"


@pytest.mark.parametrize("link_text, expected", HOME_CARDS.items())
def test_home_cards_open_the_right_page(page, base_url, link_text, expected):
    page.goto(base_url)
    page.locator(".grid.cards").get_by_role("link", name=link_text, exact=True).click()
    assert heading(page) == expected


@pytest.mark.parametrize("tab", ["Key Concepts", "User Guide", "Tutorials", "Developer Guide", "Reference"])
def test_top_tabs_navigate(page, base_url, tab):
    page.goto(base_url)
    page.locator(".md-tabs").get_by_role("link", name=tab, exact=True).click()
    assert heading(page) == tab


def test_search_finds_ndvi_tutorial(page, base_url):
    page.goto(base_url)
    page.locator(".md-search__button").click()
    page.get_by_role("combobox", name="Search").press_sequentially("NDVI", delay=30)
    first_result = page.get_by_role("option").first
    first_result.wait_for()
    assert "tutorials/ndvi-monitoring/" in first_result.get_attribute("href")
