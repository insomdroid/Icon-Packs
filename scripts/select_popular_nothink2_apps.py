#!/usr/bin/env python3
"""Select 1,000 Lawnicons-supported apps from Google Play public chart pages."""

import argparse
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


PACKAGE_RE = re.compile(r"^[A-Za-z0-9_]+(?:\\.[A-Za-z0-9_]+)+$")
CHARTS = (
    ("topselling_free", "Top Free"),
    ("topgrossing", "Top Grossing"),
)
CATEGORIES = ("APPLICATION", "GAME")
COUNTRIES = ("id", "us", "in", "gb")


def package_from_component(component):
    match = re.search(r"ComponentInfo\\{([^/]+)/", component or "")
    return match.group(1) if match else None


class ChartPackageParser(HTMLParser):
    """Collect package IDs exposed by Google Play chart cards."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.packages = []
        self.seen = set()

    def add(self, value):
        if not value:
            return
        value = unescape(value).strip()
        if PACKAGE_RE.fullmatch(value) and value not in self.seen:
            self.seen.add(value)
            self.packages.append(value)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.add(values.get("data-docid"))
        self.add(values.get("data-item-id"))

        href = values.get("href", "")
        if href:
            parsed = urlparse(href)
            for package in parse_qs(parsed.query).get("id", []):
                self.add(package)


def fetch_chart(country, category, collection):
    url = (
        "https://play.google.com/store/apps/collection/"
        f"{collection}?hl=en&gl={country.upper()}&category={category}"
    )
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    last_error = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", errors="replace")
            parser = ChartPackageParser()
            parser.feed(html)
            if not parser.packages:
                raise RuntimeError(
                    "Google Play returned a page but no chart package IDs were found"
                )
            return parser.packages
        except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2 ** attempt)

    raise RuntimeError(f"Unable to read chart {url}: {last_error}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()

    source_filter = args.upstream / "app/assets/appfilter.xml"
    svgs = args.upstream / "svgs"
    if not source_filter.is_file() or not svgs.is_dir():
        raise SystemExit("Pinned Lawnicons source archive is incomplete")
    if args.limit < 1:
        raise SystemExit("--limit must be greater than zero")

    available = set()
    for item in ET.parse(source_filter).getroot().findall("item"):
        package = package_from_component(item.get("component"))
        drawable = item.get("drawable")
        if package and drawable and (svgs / (drawable + ".svg")).is_file():
            available.add(package)

    scores = defaultdict(float)
    successful_lists = 0
    for country in COUNTRIES:
        for category in CATEGORIES:
            for collection, chart_name in CHARTS:
                try:
                    entries = fetch_chart(country, category, collection)
                except Exception as error:
                    print(
                        f"Chart unavailable: {country}/{category}/{chart_name}: {error}",
                        file=sys.stderr,
                    )
                    continue

                successful_lists += 1
                for rank, package in enumerate(entries[:200], start=1):
                    scores[package] += 1.0 / rank

                print(
                    f"Read {len(entries[:200])} entries: "
                    f"{country}/{category}/{chart_name}"
                )

    ranked = sorted(
        ((package, score) for package, score in scores.items() if package in available),
        key=lambda item: (-item[1], item[0]),
    )
    if len(ranked) < args.limit:
        raise SystemExit(
            f"Only {len(ranked)} chart-ranked apps have Lawnicons artwork; "
            f"need {args.limit}. Successful charts: {successful_lists}/16. "
            "Refusing to fill the catalog with unranked apps."
        )

    selected = ranked[:args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(package + "\\n" for package, _ in selected),
        encoding="utf-8",
    )
    print(
        f"Selected {len(selected)} apps from {len(ranked)} Lawnicons-supported "
        f"chart-ranked packages using {successful_lists}/16 Google Play charts."
    )


if __name__ == "__main__":
    main()
