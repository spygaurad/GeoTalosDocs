# GeoTALOS documentation

Source of the GeoTALOS documentation site: https://spygaurad.github.io/GeoTalosDocs/

Built with [Zensical](https://zensical.org). Pages are Markdown files in `docs/`, and the site configuration is `zensical.toml`.

## Preview locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/zensical serve
```

Open http://localhost:8000/GeoTalosDocs/. The preview reloads when you save a file.

## Where things live

| Path | What |
|---|---|
| `docs/` | The pages. The navigation order is the `nav` list in `zensical.toml`. |
| `docs/assets/` | Images and the logo |
| `docs/stylesheets/` | Custom styles, one file per concern: `brand.css` (colours), `typography.css`, `components.css` (cards, video, tables), `accessibility.css`, `responsive.css` (loaded last) |
| `tools/docs_checks/` | Checks for the page source: broken links and anchors, leftover placeholders, dashes |
| `tests/e2e/` | Browser tests of the built site |
| `.github/workflows/check.yml` | Runs all tests and checks on every push and pull request |
| `.github/workflows/docs.yml` | Publishes the site to GitHub Pages on every push to `main` |

## Writing guide

- Write for ecologists first; keep developer detail in the Developer Guide.
- Use the exact button and field names from the GeoTALOS interface, in **bold**.
- Check facts against the code or the paper before writing them.
- No em dashes, en dashes or `" - "` used as a dash. Use a period, comma, colon or parentheses.
- No screenshots for now, text only. Short video clips will be added later.

## Run the checks and tests

```bash
.venv/bin/zensical build --clean                  # build the site into site/
.venv/bin/python -m tools.docs_checks docs        # links, placeholders, dashes
.venv/bin/python -m pytest tools -q               # unit tests for the checks
.venv/bin/python -m playwright install chromium   # once, for the browser tests
.venv/bin/python -m pytest tests/e2e -q           # browser tests on site/
```

To run the browser tests with an installed Chrome instead of Playwright's Chromium, set `E2E_BROWSER_CHANNEL=chrome`.

## Publishing

Open a pull request into `main`. When the **Checks** workflow passes and the pull request is merged, the **Documentation** workflow builds and publishes the site.
