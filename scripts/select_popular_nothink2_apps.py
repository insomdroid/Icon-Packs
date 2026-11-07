#!/usr/bin/env python3
"""Select 1,000 Lawnicons-supported apps using Google Play chart rankings."""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from google_play_scraper import Category, Collection, collections


def package_from_component(component):
    match = re.search(r"ComponentInfo\{([^/]+)/", component or "")
    return match.group(1) if match else None


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

    available = set()
    for item in ET.parse(source_filter).getroot().findall("item"):
        package = package_from_component(item.get("component"))
        drawable = item.get("drawable")
        if package and drawable and (svgs / (drawable + ".svg")).is_file():
            available.add(package)

    scores = defaultdict(float)
    successful_lists = 0
    for country in ("id", "us", "in", "gb"):
        for category in (Category.APPLICATION, Category.GAME):
            for chart in (Collection.TOP_FREE, Collection.GROSSING):
                try:
                    entries = collections(
                        collection=chart,
                        category=category,
                        results=200,
                        lang="en",
                        country=country,
                    )
                except Exception as error:
                    print(
                        f"Chart unavailable: {country}/{category.name}/{chart.name}: {error}",
                        file=sys.stderr,
                    )
                    continue
                successful_lists += 1
                for rank, entry in enumerate(entries, start=1):
                    package = entry.get("appId")
                    if package:
                        scores[package] += 1.0 / rank

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
