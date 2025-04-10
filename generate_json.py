#!/usr/bin/env python3
import os
import yaml
import csv
import json
from pathlib import Path

def load_routes_config():
    """Load routes configuration from YAML file"""
    with open('config/routes.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def read_csv_timetable(csv_path):
    """Read timetable from CSV file and convert to a flat list format with numeric time and minute values"""
    timetable_list = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:  # Skip empty rows
                continue
            # Convert hour to integer
            hour = int(row[0])
            # Join all minute columns and split by space
            minutes_str = ' '.join(row[1:])
            # Convert each minute to an integer
            minutes = [int(m) for m in minutes_str.split() if m]
            # Append a dictionary for each minute with keys "time" and "minute"
            for m in minutes:
                timetable_list.append({"time": hour, "minute": m})
    return timetable_list

def generate_json_files():
    """Generate route JSON files for all routes and paths; output to data/route/"""
    config = load_routes_config()
    output_dir = os.path.join('data', 'route')
    os.makedirs(output_dir, exist_ok=True)

    for route_id, route_data in config['routes'].items():
        for path_id, path_data in route_data['paths'].items():
            # Process each day type (weekday, saturday, sunday)
            for day_type, csv_file in path_data['csv_files'].items():
                if not os.path.exists(csv_file):
                    print(f"Warning: CSV file {csv_file} not found")
                    continue

                json_data = {
                    "route_id": route_id,
                    "path_id": path_id,
                    "name": path_data['name'],
                    "origin": path_data['origin'],
                    "destination": path_data['stops'][-1]['name'],
                    "via": path_data.get('via', []),
                    "stops": path_data['stops'],
                    "timetable": read_csv_timetable(csv_file)
                }

                output_file = os.path.join(output_dir, f"{path_id}_{day_type}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                print(f"Generated {output_file}")

def generate_aggregated_json_files():
    """Generate aggregated JSON files for each sfc_direction and schedule type; output to data/aggregated/"""
    config = load_routes_config()
    aggregated = {
        'to_weekday': [],
        'to_saturday': [],
        'to_sunday': [],
        'from_weekday': [],
        'from_saturday': [],
        'from_sunday': []
    }

    for route_id, route_data in config['routes'].items():
        for path_id, path_data in route_data['paths'].items():
            sfc_direction = path_data.get('sfc_direction', '').lower()
            if sfc_direction not in ['to', 'from']:
                print(f"Warning: Invalid or missing sfc_direction for {route_id} {path_id}")
                continue

            for schedule_type, csv_file in path_data.get('csv_files', {}).items():
                if not os.path.exists(csv_file):
                    print(f"Warning: CSV file {csv_file} not found")
                    continue

                times = read_csv_timetable(csv_file)
                for entry in times:
                    # Compute the total minutes after midnight from the entry (dictionary with 'time' and 'minute')
                    total_minutes = entry["time"] * 60 + entry["minute"]
                    record = {
                        "time": total_minutes,  # e.g., 643 for 10:43
                        "scheduleType": schedule_type,
                        "routeCode": route_id,
                        "dest": path_data.get("destination", path_data["stops"][-1]['name'] if path_data.get("stops") else ""),
                        "start": path_data.get("origin", ""),
                        "additionalInfo": path_data.get("name", ""),
                        "metadata": {
                            "stops": path_data.get("stops", [])
                        }
                    }
                    agg_key = f"{sfc_direction}_{schedule_type}"
                    aggregated[agg_key].append(record)

    # Sort each aggregated list by time
    for key in aggregated:
        aggregated[key].sort(key=lambda x: x["time"])

    output_dir = os.path.join("data", "aggregated")
    os.makedirs(output_dir, exist_ok=True)

    for key, records in aggregated.items():
        output_file = os.path.join(output_dir, f"{key}.json")
        with open(output_file, 'w', encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"Generated {output_file}")

def main():
    generate_json_files()
    generate_aggregated_json_files()

if __name__ == "__main__":
    main()