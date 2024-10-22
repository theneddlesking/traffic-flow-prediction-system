import pandas as pd
import requests
import sqlite3

db_path = "../db/site.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#testing
def test_api_call(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print(f"API call failed with status code: {response.status_code}")



def get_location_id(lat, long):
    cursor.execute("SELECT location_id FROM locations WHERE latitude = ? AND longitude = ?", (lat, long))
    result = cursor.fetchone()
    return result[0] if result else None

def get_time_from_model(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("routes", [])[0].get("hours_taken", None)
    return None

def get_location_id(lat, long):
    cursor.execute("SELECT location_id FROM locations WHERE lat = ? AND long = ?", (lat, long))
    result = cursor.fetchone()
    return result[0] if result else None

def calculate_accuracy(predicted_time, actual_time):
    if actual_time == 0:
        return 0
    return 100 - abs((predicted_time - actual_time) / actual_time * 100)

def compare_time_taken(input_file):
    df = pd.read_csv(input_file)

    results = []

    # Iterate over each row in the truedataCSV and compare them against basic_predictions

    for index, row in df.iterrows():
        start_lat = row['START_LAT']
        start_long = row['START_LONG']
        end_lat = row['END_LAT']
        end_long = row['END_LONG']
        actual_time = row['Time_Taken']
        time_of_day = row['Time']
    return

test_api_call(43, 71, '12:00') #testing

input_file = '../true_data/cleanTrueData.csv'