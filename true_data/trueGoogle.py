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
    start_point = (float(start_lat), float(start_long))
    end_point = (float(end_lat), float(end_long))
    return geodesic(start_point, end_point).kilometers


def get_travel_time(start_lat, start_long, end_lat, end_long, departure_time):

    distance = calculate_distance(start_lat, start_long, end_lat, end_long)
    if distance < 0.1:
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

def simulate_times_and_days(start_lat, start_long, end_lat, end_long):
    times_of_day = [(7, 0), (12, 0), (18, 0)]
    days_of_week = {'Monday': 0, 'Friday': 4, 'Saturday': 5}

    results = {}
    for day_name, day_num in days_of_week.items():
        results[day_name] = {}
        for hour, minute in times_of_day:
            departure_time = get_unix_timestamp(day_num, hour, minute)
            duration = get_travel_time(start_lat, start_long, end_lat, end_long, departure_time)
            results[day_name][f"{hour}:{minute}"] = duration
            print(f"{day_name} at {hour}:{minute}: {duration}")
    
    return results

def main(input_csv, output_csv):
    route_table = set()
    route_id = 1

    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = ['Route_ID', 'START_LAT', 'START_LONG', 'END_LAT', 'END_LONG', 'Day', 'Time', 'Time_Taken']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for start_row in rows:
            start_lat = start_row['NB_LATITUDE']
            start_long = start_row['NB_LONGITUDE']

            for end_row in rows:
                end_lat = end_row['NB_LATITUDE']
                end_long = end_row['NB_LONGITUDE']

                # Skip identical start and end points
                if start_lat == end_lat and start_long == end_long:
                    continue

                # Check if this route already exists in the route_table
                route_key = (start_lat, start_long, end_lat, end_long)
                if route_key in route_table:
                    continue  # Skip if route already exists

                # Add the new route to the route_table
                route_table.add(route_key)

                results = simulate_times_and_days(start_lat, start_long, end_lat, end_long)

                for day, times in results.items():
                    for time_of_day, duration in times.items():
                        writer.writerow({
                            'Route_ID': route_id,
                            'START_LAT': start_lat,
                            'START_LONG': start_long,
                            'END_LAT': end_lat,
                            'END_LONG': end_long,
                            'Day': day,
                            'Time': time_of_day,
                            'Time_Taken': duration
                        })
                        route_id += 1


if __name__ == '__main__':
    input_csv = '../data/vic/ScatsOctober2006.csv'
    output_csv = 'trueData.csv'
    main(input_csv, output_csv)
