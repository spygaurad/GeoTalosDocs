"""Theme, layout and accessibility behaviour in the browser."""

import pytest

from .conftest import site_pages


def test_theme_toggle_reaches_dark_mode(page, base_url):
    page.goto(base_url)
    scheme = lambda: page.evaluate("document.body.getAttribute('data-md-color-scheme')")
    # The toggle cycles system, light, dark; click until dark or give up.
    for _ in range(3):
        if scheme() == "slate":
            break
        page.locator("label[for^=__palette]:visible").first.click()
    assert scheme() == "slate"


@pytest.mark.parametrize("path", site_pages())
def test_no_sideways_scroll_on_a_phone(browser, base_url, path):
    context = browser.new_context(viewport={"width": 375, "height": 800})
    page = context.new_page()
    page.goto(base_url + path)
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    context.close()
    assert overflow <= 0, f"{path} scrolls sideways by {overflow}px at 375px"


FOCUSABLE_TO_CHECK = 15


def test_keyboard_focus_ring_is_visible(page, base_url):
    """Tab through the first controls; each must show a visible focus outline.

    For the theme toggle the focused element is a hidden radio input, so the
    outline is checked on the label right after it.
    """
    page.goto(base_url)
    for _ in range(FOCUSABLE_TO_CHECK):
        page.keyboard.press("Tab")
        name, style, width = page.evaluate(
            """() => {
                let el = document.activeElement;
                if (el.matches('input.md-option')) el = el.nextElementSibling;
                const s = getComputedStyle(el);
                return [(el.textContent || el.getAttribute('title') || el.tagName).trim().slice(0, 30),
                        s.outlineStyle, s.outlineWidth];
            }"""
        )
        assert style != "none" and width != "0px", f"no focus ring on {name!r}"
