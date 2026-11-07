#!/usr/bin/env python3
"""Select popular Lawnicons-supported apps using the maintained Google Play scraper CLI."""

import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


PACKAGE_RE = re.compile(r"^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+$")
CHARTS = (
    ("TOP_FREE", "Top Free"),
    ("GROSSING", "Top Grossing"),
)
CATEGORIES = ("APPLICATION", "GAME")
COUNTRIES = ("id", "us", "in", "gb")


def package_from_component(component):
    match = re.search(r"ComponentInfo\{([^/]+)/", component or "")
    return match.group(1) if match else None


def fetch_chart(country, category, collection):
    command = [
        "google-play-scraper",
        "list",
        "--collection", collection,
        "--category", category,
        "--num", "200",
        "--country", country,
        "--lang", "en",
        "--throttle", "1",
    ]
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Scraper returned invalid JSON: {result.stdout[:500]!r}"
        ) from error

    if not isinstance(payload, list):
        raise RuntimeError(
            f"Expected a JSON list, received {type(payload).__name__}"
        )

    packages = []
    seen = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        package = item.get("appId") or item.get("app_id")
        if isinstance(package, str) and PACKAGE_RE.fullmatch(package):
            if package not in seen:
                seen.add(package)
                packages.append(package)

    if not packages:
        raise RuntimeError(
            f"Scraper returned {len(payload)} chart rows but no valid app IDs"
        )
    return packages


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
        "".join(package + "\n" for package, _ in selected),
        encoding="utf-8",
    )
    print(
        f"Selected {len(selected)} apps from {len(ranked)} Lawnicons-supported "
        f"chart-ranked packages using {successful_lists}/16 Google Play charts."
    )


if __name__ == "__main__":
    main()
