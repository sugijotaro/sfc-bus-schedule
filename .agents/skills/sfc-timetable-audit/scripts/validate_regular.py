#!/usr/bin/env python3
"""Validate the local structure of the supported regular SFC timetables."""

import csv
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
ROUTES_FILE = ROOT / "config/routes.yaml"
SUPPORTED_ROUTES = {"sho19", "sho23", "sho24", "sho25", "sho28"}


def main() -> int:
    config = yaml.safe_load(ROUTES_FILE.read_text(encoding="utf-8"))
    routes = config.get("routes", {})
    actual_routes = set(routes)
    errors = []

    if actual_routes != SUPPORTED_ROUTES:
        added = sorted(actual_routes - SUPPORTED_ROUTES)
        missing = sorted(SUPPORTED_ROUTES - actual_routes)
        errors.append(
            "supported route set changed; update this skill first "
            f"(added={added}, missing={missing})"
        )

    checked_files = set()
    for route_id, route in routes.items():
        for path_id, path in route.get("paths", {}).items():
            stops = path.get("stops", [])
            if not stops:
                errors.append(f"{path_id}: no stops")
                continue

            if path.get("origin") != stops[0].get("name"):
                errors.append(
                    f"{path_id}: origin {path.get('origin')!r} != first stop "
                    f"{stops[0].get('name')!r}"
                )

            if path_id != "sho19_to" and path.get("destination") != stops[-1].get("name"):
                errors.append(
                    f"{path_id}: destination {path.get('destination')!r} != last stop "
                    f"{stops[-1].get('name')!r}"
                )

            for day_type, relative_path in path.get("csv_files", {}).items():
                if day_type not in {"weekday", "saturday", "sunday"}:
                    errors.append(f"{path_id}: non-regular day type {day_type!r}")
                    continue

                csv_path = ROOT / relative_path
                checked_files.add(relative_path)
                if not csv_path.is_file():
                    errors.append(f"missing CSV: {relative_path}")
                    continue

                with csv_path.open(encoding="utf-8", newline="") as handle:
                    for row_number, row in enumerate(csv.reader(handle), start=1):
                        if not row or not row[0]:
                            continue
                        try:
                            hour = int(row[0])
                            minutes_text = " ".join(row[1:]).strip()
                            minute_tokens = minutes_text.split() if minutes_text else []
                            minutes = [int(token) for token in minute_tokens]
                        except ValueError:
                            errors.append(f"{relative_path}:{row_number}: non-numeric time")
                            continue

                        if not 0 <= hour <= 25:
                            errors.append(f"{relative_path}:{row_number}: invalid hour {hour}")
                        if minutes != sorted(minutes):
                            errors.append(f"{relative_path}:{row_number}: minutes not sorted")
                        if len(minutes) != len(set(minutes)):
                            errors.append(f"{relative_path}:{row_number}: duplicate minute")
                        if any(not 0 <= minute <= 59 for minute in minutes):
                            errors.append(f"{relative_path}:{row_number}: invalid minute")
                        if any(len(token) != 2 for token in minute_tokens):
                            errors.append(f"{relative_path}:{row_number}: minute not zero-padded")

    if errors:
        print("Regular timetable validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Regular timetable structure is valid: "
        f"{len(actual_routes)} routes, {len(checked_files)} CSV files."
    )
    print("Special schedules were not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
