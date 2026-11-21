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


def test_left_panel_and_full_width_prose_on_desktop(browser, base_url):
    """Navigation lives in the left panel (no top tabs) and prose is not capped."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto(base_url + "user-guide/getting-started/")
    assert page.locator(".md-tabs").count() == 0
    panel = page.locator(".md-sidebar--primary")
    for section in ["Key Concepts", "User Guide", "Tutorials", "Developer Guide", "Reference"]:
        assert panel.get_by_role("link", name=section, exact=True).is_visible(), section
    max_width = page.evaluate("getComputedStyle(document.querySelector('.md-typeset > p')).maxWidth")
    context.close()
    assert max_width == "none"


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


def _channels(css: str) -> list[float]:
    """'rgb(1, 2, 3)' or 'rgba(1, 2, 3, 0.5)' as [r, g, b, alpha]."""
    parts = [float(v) for v in css[css.index("(") + 1 : css.index(")")].split(",")]
    return parts + [1.0] if len(parts) == 3 else parts


def _luminance(color: str, background: str) -> float:
    """Brightness of a text colour as seen on the page background (theme colours are translucent)."""
    *fg, alpha = _channels(color)
    bg = _channels(background)[:3]
    r, g, b = (f * alpha + k * (1 - alpha) for f, k in zip(fg, bg))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_left_panel_sections_stand_out_from_pages(browser, base_url, scheme):
    """Top level sections are larger, bolder and stronger than the pages inside them."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, color_scheme=scheme)
    page = context.new_page()
    page.goto(base_url + "concepts/workflows/")
    style = "el => { const s = getComputedStyle(el); return [parseFloat(s.fontSize), parseInt(s.fontWeight), s.color]; }"
    panel = page.locator(".md-sidebar--primary")
    top = panel.get_by_role("link", name="Key Concepts", exact=True).evaluate(style)
    inner = panel.get_by_role("link", name="Annotation sets", exact=True).evaluate(style)
    bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    context.close()
    assert top[0] > inner[0], "section font is not larger"
    assert top[1] > inner[1], "section font is not bolder"
    if scheme == "light":
        assert _luminance(top[2], bg) < _luminance(inner[2], bg), "section is not darker"
    else:
        assert _luminance(top[2], bg) > _luminance(inner[2], bg), "section is not brighter on dark"


@pytest.mark.parametrize("path", ["concepts/workflows/", "developer/tiles/", "tutorials/ndvi-monitoring/"])
def test_figures_load_and_fit(page, base_url, path):
    page.goto(base_url + path)
    images = page.locator("figure.doc-figure img")
    assert images.count() > 0
    for i in range(images.count()):
        img = images.nth(i)
        img.scroll_into_view_if_needed()
        assert img.evaluate("el => el.complete && el.naturalWidth > 0"), f"image {i} did not load"
        assert img.bounding_box()["height"] <= 26 * 16 + 1, f"image {i} is too tall"
