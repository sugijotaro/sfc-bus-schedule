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
    """Generate JSON files for all routes and paths"""
    config = load_routes_config()
    os.makedirs('data', exist_ok=True)

    for route_id, route_data in config['routes'].items():
        for path_id, path_data in route_data['paths'].items():
            # Process each day type (weekday, saturday, sunday)
            for day_type, csv_file in path_data['csv_files'].items():
                if not os.path.exists(csv_file):
                    print(f"Warning: CSV file {csv_file} not found")
                    continue

                # Generate JSON data
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

                # Save JSON file
                output_file = f"data/{path_id}_{day_type}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_json_files()