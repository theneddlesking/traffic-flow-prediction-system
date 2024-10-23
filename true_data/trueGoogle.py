#pip install geopy

import os
import csv
import requests
import time
from datetime import datetime, timedelta
from geopy.distance import geodesic

API_KEY = os.getenv('GOOGLE_API_KEY')

def get_unix_timestamp(day_of_week, hour, minute=0):
    today = datetime.now()
    days_ahead = (day_of_week - today.weekday() + 7) % 7
    target_date = today.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if days_ahead > 0:
        target_date += timedelta(days=days_ahead)

    return int(time.mktime(target_date.timetuple()))

def calculate_distance(start_lat, start_long, end_lat, end_long):
    """Calculate the distance between two sets of coordinates."""
    start_point = (float(start_lat), float(start_long))
    end_point = (float(end_lat), float(end_long))
    return geodesic(start_point, end_point).kilometers

def get_travel_time(start_lat, start_long, end_lat, end_long, departure_time):
    """Call the Google Maps API to get travel time between two points at a given time."""
    distance = calculate_distance(start_lat, start_long, end_lat, end_long)
    if distance < 1:
        print(f"Skipping route due to short distance: {distance} km between {start_lat},{start_long} and {end_lat},{end_long}")
        return "Too close - Skipped"

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_lat},{start_long}&destination={end_lat},{end_long}"
        f"&departure_time={departure_time}&key={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"API Response for route {start_lat},{start_long} to {end_lat},{end_long}: {data}")
        if data['status'] == 'OK':
            duration = data['routes'][0]['legs'][0]['duration_in_traffic']['text']
            return duration
        else:
            print(f"Error: {data['status']}")
            return "Error"
    else:
        print(f"Error: {response.status_code}")
        return "Error"

def simulate_times(start_lat, start_long, end_lat, end_long):
    """Simulate routes at different times of the day without considering the day."""
    times_of_day = [(11, 0), (17, 0)]  # Morning, Noon, Evening

    results = {}
    for hour, minute in times_of_day:
        departure_time = get_unix_timestamp(0, hour, minute)  # Use Monday as base
        duration = get_travel_time(start_lat, start_long, end_lat, end_long, departure_time)
        results[f"{hour}:{minute}"] = duration
        print(f"Time {hour}:{minute}: {duration}")
    
    return results

def main(input_csv, output_csv, max_routes=200):
    """Process the routes and limit output to 200 diverse routes, prioritizing longer routes."""
    route_table = set()
    route_id = 1
    valid_routes_count = 0
    start_used = set()

    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = ['Route_ID', 'START_LAT', 'START_LONG', 'END_LAT', 'END_LONG', 'Time', 'Time_Taken', 'Distance']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Sort routes by distance (longer routes first)
        sorted_routes = sorted(rows, key=lambda row: calculate_distance(row['NB_LATITUDE'], row['NB_LONGITUDE'], row['NB_LATITUDE'], row['NB_LONGITUDE']), reverse=True)

        for start_row in sorted_routes:
            start_lat = start_row['NB_LATITUDE']
            start_long = start_row['NB_LONGITUDE']

            # Ensure we do not reuse the same start lat/long
            if (start_lat, start_long) in start_used:
                continue
            start_used.add((start_lat, start_long))

            for end_row in sorted_routes:
                end_lat = end_row['NB_LATITUDE']
                end_long = end_row['NB_LONGITUDE']

                # Skip identical start and end points
                if start_lat == end_lat and start_long == end_long:
                    continue

                route_key = (start_lat, start_long, end_lat, end_long)
                if route_key in route_table:
                    continue  # Skip if route already exists

                # Add the new route to the route_table
                route_table.add(route_key)

                distance = calculate_distance(start_lat, start_long, end_lat, end_long)
                results = simulate_times(start_lat, start_long, end_lat, end_long)

                for time_of_day, duration in results.items():
                    if duration not in ["Error", "Too close - Skipped"]:  # Filter out errors and skipped routes
                        writer.writerow({
                            'Route_ID': route_id,
                            'START_LAT': start_lat,
                            'START_LONG': start_long,
                            'END_LAT': end_lat,
                            'END_LONG': end_long,
                            'Time': time_of_day,
                            'Time_Taken': duration,
                            'Distance': distance
                        })
                        route_id += 1
                        valid_routes_count += 1

                    # Stop when 200 valid routes have been written
                    if valid_routes_count >= max_routes:
                        print(f"Reached the maximum limit of {max_routes} routes.")
                        return

if __name__ == '__main__':
    input_csv = '../data/vic/ScatsOctober2006.csv'
    output_csv = 'NewEvaluation.csv'
    main(input_csv, output_csv)
