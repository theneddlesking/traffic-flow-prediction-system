import pandas as pd
import requests
import sqlite3

db_path = "../db/site.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def get_location_id(lat, long):

    return

def get_time_from_model(start_location_id, end_location_id, time_of_day):

    return None

def compare_time_taken():
    
    return


input_file = '../true_data/cleanTrueData.csv'