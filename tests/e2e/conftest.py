"""Shared fixtures for the end-to-end tests.

The tests run against the built site in site/ (run `zensical build` first),
served by Python's own http.server on a free local port.

Browser: Playwright's bundled Chromium by default. To use an installed
Chrome instead, set E2E_BROWSER_CHANNEL=chrome.
"""

import functools
import http.server
import os
import threading
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

SITE_DIR = Path(__file__).resolve().parents[2] / "site"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def base_url():
    if not (SITE_DIR / "index.html").exists():
        pytest.fail("site/ is not built. Run `zensical build --clean` first.")
    handler = functools.partial(_QuietHandler, directory=str(SITE_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel=os.environ.get("E2E_BROWSER_CHANNEL"))
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    page = context.new_page()
    yield page
    context.close()


def site_pages() -> list[str]:
    """Every built page as a path relative to the site root, for example 'user-guide/'."""
    relative = (p.parent.relative_to(SITE_DIR).as_posix() for p in SITE_DIR.rglob("index.html"))
    return sorted("" if path == "." else f"{path}/" for path in relative)
