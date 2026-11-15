"""Readers can reach every part of the site from the home page."""

import re

import pytest
from playwright.sync_api import expect

HOME_CARDS = ["Getting started", "Tutorials", "User Guide", "Developer Guide"]
TABS = ["Key Concepts", "User Guide", "Tutorials", "Developer Guide", "Reference"]


def expect_heading(page, text: str) -> None:
    """Wait for the page title; the theme adds a ¶ permalink after it.

    Waiting matters: the site loads pages in place (instant navigation), so the
    old heading is still there for a moment after a click.
    """
    expect(page.locator("h1")).to_have_text(re.compile(rf"^{re.escape(text)}¶?$"))


def test_home_page_loads(page, base_url):
    page.goto(base_url)
    expect(page).to_have_title(re.compile(r"^Home"))
    expect_heading(page, "GeoTALOS documentation")


@pytest.mark.parametrize("link_text", HOME_CARDS)
def test_home_cards_open_the_right_page(page, base_url, link_text):
    page.goto(base_url)
    page.locator(".grid.cards").get_by_role("link", name=link_text, exact=True).click()
    expect_heading(page, link_text)


@pytest.mark.parametrize("tab", TABS)
def test_top_tabs_navigate(page, base_url, tab):
    page.goto(base_url)
    page.locator(".md-tabs").get_by_role("link", name=tab, exact=True).click()
    expect_heading(page, tab)


def test_search_finds_ndvi_tutorial(page, base_url):
    page.goto(base_url)
    page.locator(".md-search__button").click()
    page.get_by_role("combobox", name="Search").press_sequentially("NDVI", delay=30)
    expect(page.get_by_role("option").first).to_have_attribute("href", re.compile(r"tutorials/ndvi-monitoring/"))
