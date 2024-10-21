import pandas as pd
import requests
import sqlite3

db_path = "../db/site.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def get_location_id(lat, long):
    cursor.execute("SELECT location_id FROM locations WHERE latitude = ? AND longitude = ?", (lat, long))
    result = cursor.fetchone()
    return result[0] if result else None

def get_time_from_model(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("hours_taken")  # Adjust based on the actual API response format
    return None

def compare_time_taken():
    
    return


input_file = '../true_data/cleanTrueData.csv'