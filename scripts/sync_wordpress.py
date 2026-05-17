#!/usr/bin/env python3
"""
Sync docs markdown files to WordPress.com pages via the REST API.

Required env vars:
  WP_ACCESS_TOKEN  - WordPress.com OAuth access token
  WP_SITE          - Site domain, e.g. veelabs1.wordpress.com
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import markdown

SITE = os.environ["WP_SITE"]
TOKEN = os.environ["WP_ACCESS_TOKEN"]
API_BASE = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}"

# Files to sync: (source markdown path, WordPress page slug, page title, menu order)
PAGES = [
    ("docs/index.md",                  "home",           "Home",            1),
    ("docs/projects/index.md",         "projects",       "Projects",        2),
    ("docs/projects/breachguard.md",   "breachguard",    "BreachGuard",     3),
    ("docs/projects/acservice.md",     "acserviceapp",   "ACServiceApp",    4),
    ("docs/guide/index.md",            "getting-started","Getting Started", 5),
    ("docs/guide/api.md",              "api-reference",  "API Reference",   6),
    ("docs/guide/examples.md",         "examples",       "Examples",        7),
    ("docs/guide/contributing.md",     "contributing",   "Contributing",    8),
]

MARKDOWN_EXT = ["extra", "codehilite", "fenced_code", "tables", "toc"]


def md_to_html(path: str) -> str:
    with open(path) as f:
        text = f.read()
    # Strip VitePress frontmatter
    text = re.sub(r"^---\n.*?---\n", "", text, flags=re.DOTALL)
    return markdown.markdown(text, extensions=MARKDOWN_EXT)


def api(method: str, endpoint: str, data: dict | None = None) -> dict:
    url = f"{API_BASE}{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        raise


def get_existing_pages() -> dict[str, dict]:
    """Return a slug → page dict for all existing pages."""
    result = api("GET", "/posts/?type=page&number=100&fields=ID,slug,title")
    return {p["slug"]: p for p in result.get("posts", [])}


def sync_page(slug: str, title: str, html: str, order: int, existing: dict) -> None:
    payload = {
        "type": "page",
        "title": title,
        "content": html,
        "status": "publish",
        "slug": slug,
        "menu_order": order,
    }
    if slug in existing:
        page_id = existing[slug]["ID"]
        api("POST", f"/posts/{page_id}", payload)
        print(f"  Updated: {title} (ID {page_id})")
    else:
        page = api("POST", "/posts/new", payload)
        print(f"  Created: {title} (ID {page['ID']})")


def main() -> None:
    print(f"Syncing to {SITE} ...")
    existing = get_existing_pages()
    print(f"  Found {len(existing)} existing page(s): {list(existing.keys())}")

    errors = []
    for md_path, slug, title, order in PAGES:
        if not os.path.exists(md_path):
            print(f"  Skip (not found): {md_path}")
            continue
        print(f"Processing: {md_path}")
        try:
            html = md_to_html(md_path)
            sync_page(slug, title, html, order, existing)
        except Exception as exc:
            print(f"  FAILED: {exc}", file=sys.stderr)
            errors.append(md_path)

    if errors:
        print(f"\nFailed files: {errors}", file=sys.stderr)
        sys.exit(1)
    print("\nSync complete.")


if __name__ == "__main__":
    main()
