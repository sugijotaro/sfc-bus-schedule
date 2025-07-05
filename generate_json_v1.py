#!/usr/bin/env python3
import os
import yaml
import csv
import json
import copy # copyライブラリをインポート
from pathlib import Path

VERSION = "v1"

def load_routes_config():
    """Load routes configuration from YAML file"""
    with open("config/routes.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_special_schedules_config():
    """Load special schedules configuration from YAML file"""
    file_path = "config/special_schedules.yaml"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def read_csv_timetable(csv_path):
    """Read timetable from CSV file and convert to a flat list format"""
    if not os.path.exists(csv_path):
        print(f"Warning: CSV file {csv_path} not found")
        return []
    timetable_list = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            hour = int(row[0])
            minutes_str = " ".join(row[1:])
            minutes = [int(m) for m in minutes_str.split() if m]
            for m in minutes:
                timetable_list.append({"time": hour, "minute": m})
    return timetable_list

def generate_route_json(config, day_types):
    """Generate route JSON files for specified day types"""
    output_dir = os.path.join("data", VERSION, "route")
    os.makedirs(output_dir, exist_ok=True)

    for route_id, route_data in config["routes"].items():
        for path_id, path_data in route_data["paths"].items():
            for day_type in day_types:
                csv_file = path_data.get("csv_files", {}).get(day_type)
                if not csv_file:
                    continue

                json_data = {
                    "route_id": route_id,
                    "path_id": path_id,
                    "name": path_data["name"],
                    "origin": path_data["origin"],
                    "destination": path_data["stops"][-1]["name"],
                    "via": path_data.get("via", ""),
                    "stops": path_data["stops"],
                    "timetable": read_csv_timetable(csv_file),
                }

                output_file = os.path.join(output_dir, f"{path_id}_{day_type}.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                print(f"Generated {output_file}")

def generate_flat_json(config, day_types):
    """Generate aggregated flat JSON files for specified day types"""
    aggregated = {f"{direction}_{day_type}": [] for direction in ["to", "from"] for day_type in day_types}

    for route_id, route_data in config["routes"].items():
        for path_id, path_data in route_data["paths"].items():
            sfc_direction = path_data.get("sfc_direction", "").lower()
            if sfc_direction not in ["to", "from"]:
                continue

            for day_type in day_types:
                csv_file = path_data.get("csv_files", {}).get(day_type)
                if not csv_file:
                    continue
                
                times = read_csv_timetable(csv_file)
                for entry in times:
                    hour = entry["time"]
                    minute = entry["minute"]
                    unique_id = f"{route_id}{hour:02d}{minute:02d}"
                    record = {
                        "id": unique_id,
                        "time": hour,
                        "minute": minute,
                        "scheduleType": day_type,
                        "routeCode": route_id,
                        "routeName": route_data.get("name", ""),
                        "name": path_data.get("name", ""),
                        "origin": path_data.get("origin", ""),
                        "destination": path_data.get("destination", path_data["stops"][-1]["name"] if path_data.get("stops") else ""),
                        "via": path_data.get("via", ""),
                        "sfc_direction": f"{sfc_direction}_sfc",
                        "metadata": {},
                    }
                    departure_total = hour * 60 + minute
                    new_stops = []
                    for stop in path_data.get("stops", []):
                        offset = stop.get("cumulative_time", 0)
                        arrival_total = departure_total + offset
                        arrival_hour = arrival_total // 60
                        arrival_minute = arrival_total % 60
                        new_stop = stop.copy()
                        new_stop["arrival"] = {"time": arrival_hour, "minute": arrival_minute}
                        new_stops.append(new_stop)
                    record["metadata"]["stops"] = new_stops

                    agg_key = f"{sfc_direction}_{day_type}"
                    aggregated[agg_key].append(record)

    output_dir = os.path.join("data", VERSION, "flat")
    os.makedirs(output_dir, exist_ok=True)
    
    for key, records in aggregated.items():
        if not records: continue
        records.sort(key=lambda x: x["time"] * 60 + x["minute"])
        direction, day = key.split("_", 1)
        output_file = os.path.join(output_dir, f"{direction}_sfc_{day}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"Generated {output_file}")

def generate_special_schedules_metadata(special_schedules_config):
    """Generate a metadata file for special schedules"""
    if not special_schedules_config or "special_schedules" not in special_schedules_config:
        return
        
    metadata = []
    for schedule in special_schedules_config["special_schedules"]:
        metadata.append({
            "date": schedule["date"],
            "description": schedule["description"],
            "type": schedule["type"]
        })
    
    output_dir = os.path.join("data", VERSION)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "special_schedules.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Generated {output_file}")


def main():
    base_config = load_routes_config()
    special_schedules_config = load_special_schedules_config()

    # 1. Generate regular schedules (weekday, saturday, sunday)
    print("--- Generating Regular Schedules ---")
    regular_day_types = ["weekday", "saturday", "sunday"]
    generate_route_json(base_config, regular_day_types)
    generate_flat_json(base_config, regular_day_types)

    # 2. Generate special schedules if defined
    if special_schedules_config and "special_schedules" in special_schedules_config:
        print("\n--- Generating Special Schedules ---")
        for schedule in special_schedules_config["special_schedules"]:
            print(f"Processing special schedule for {schedule['date']} ({schedule['type']})")
            temp_config = copy.deepcopy(base_config)
            day_type = schedule["type"]

            # Override csv_files in temp_config
            for route_id, paths in schedule["overrides"].items():
                for path_id, csv_file in paths.items():
                    if route_id in temp_config["routes"] and path_id in temp_config["routes"][route_id]["paths"]:
                        # Clear existing day types and set only the special one
                        temp_config["routes"][route_id]["paths"][path_id]["csv_files"] = {
                            day_type: csv_file
                        }
                    else:
                        print(f"Warning: {route_id}/{path_id} not found in routes.yaml, skipping override.")
            
            # Generate JSON for this special schedule
            generate_route_json(temp_config, [day_type])
            generate_flat_json(temp_config, [day_type])

        # 3. Generate special schedules metadata file
        print("\n--- Generating Special Schedules Metadata ---")
        generate_special_schedules_metadata(special_schedules_config)

if __name__ == "__main__":
    main()