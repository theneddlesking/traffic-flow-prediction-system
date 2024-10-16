import os
import csv
import requests
import time
from datetime import datetime

# Get API key from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')

# Function to convert date and time into Unix timestamp (Google API uses Unix time)
def get_unix_timestamp(day_of_week, hour, minute=0):
    today = datetime.now()
    target_date = today

    days_ahead = (day_of_week - today.weekday() + 7) % 7
    target_date = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if days_ahead > 0:
        target_date = target_date + timedelta(days=days_ahead)

    return int(time.mktime(target_date.timetuple()))

def get_travel_time(start_lat, start_long, end_lat, end_long, departure_time):
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_lat},{start_long}&destination={end_lat},{end_long}"
        f"&departure_time={departure_time}&key={API_KEY}"
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            duration = data['routes'][0]['legs'][0]['duration_in_traffic']['text']
            return duration
        else:
            print(f"Error: {data['status']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

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
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['START_LAT', 'START_LONG', 'END_LAT', 'END_LONG', 'Day', 'Time', 'Time_Taken']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            start_lat = row['START_LAT']
            start_long = row['START_LONG']
            end_lat = row['END_LAT']
            end_long = row['END_LONG']

            results = simulate_times_and_days(start_lat, start_long, end_lat, end_long)
            for day, times in results.items():
                for time_of_day, duration in times.items():
                    writer.writerow({
                        'START_LAT': start_lat,
                        'START_LONG': start_long,
                        'END_LAT': end_lat,
                        'END_LONG': end_long,
                        'Day': day,
                        'Time': time_of_day,
                        'Time_Taken': duration
                    })

if __name__ == '__main__':
    input_csv = '../data/vic/ScatsOctober2006.csv'  
    output_csv = 'output_file.csv'
    main(input_csv, output_csv)
