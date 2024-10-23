import pandas as pd
import requests
import sqlite3
from sklearn.metrics import f1_score
import re

db_path = "site.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def get_location_id(lat, long):
    cursor.execute("SELECT id FROM locations WHERE lat = ? AND long = ?", (lat, long))
    result = cursor.fetchone()
    return result[0] if result else None

def get_time_from_model(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        #print(f"API Response: {data}")  # Print the full response

        if 'routes' in data and len(data['routes']) > 0:
            return data['routes'][0].get('hours_taken')  # Get hours taken from the first route
        else:
            print("No routes found in the API response")
            return None
    else:
        print(f"API call failed with status code: {response.status_code}")
    return None

def parse_actual_time(actual_time_str):
    #Regex pattern to capture hours and minutes
    pattern = r"(\d+)\s*hours?\s*(\d+)?\s*mins?"
    match = re.search(pattern, actual_time_str)
    
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours + (minutes / 60)
    
    # Handle where time is in min
    if "mins" in actual_time_str:
        minutes = int(re.search(r"(\d+)\s*mins?", actual_time_str).group(1))
        return minutes / 60
    
    return None

def calculate_accuracy(predicted_time, actual_time):
    if actual_time == 0:
        return 0
    return 100 - abs((predicted_time - actual_time) / actual_time * 100)

def calculate_f1_score(y_true, y_pred, threshold=5):
    """
    Calculate the F1-score by treating the times as close or not close based on a threshold.
    If the predicted time is within a certain range (e.g., 5 minutes) of the actual time, consider it a "True Positive".
    """
    y_true_binary = [1 if abs(a - p) <= threshold else 0 for a, p in zip(y_true, y_pred)]
    y_pred_binary = [1 if abs(a - p) <= threshold else 0 for a, p in zip(y_true, y_pred)]
    
    f1 = f1_score(y_true_binary, y_pred_binary)
    return f1

def compare_time_taken(input_file):
    df = pd.read_csv(input_file)

    results = []
    total_accuracy = 0
    valid_rows = 0 

    actual_times = []
    predicted_times = []

    for index, row in df.iterrows():
        start_lat = row['START_LAT']
        start_long = row['START_LONG']
        end_lat = row['END_LAT']
        end_long = row['END_LONG']
        actual_time_str = row['Time_Taken']
        time_of_day = row['Time']

        #Parse actual_time from string to float
        actual_time = parse_actual_time(actual_time_str)

        start_location_id = get_location_id(start_lat, start_long)
        end_location_id = get_location_id(end_lat, end_long)

        if start_location_id and end_location_id and actual_time is not None:
            predicted_time = get_time_from_model(start_location_id, end_location_id, time_of_day)
            print(f"{predicted_time}")
            
            if predicted_time is not None:
                
                accuracy = calculate_accuracy(predicted_time, actual_time)
                total_accuracy += accuracy
                valid_rows += 1

                # Collect actual and predicted times for F1-score calculation
                actual_times.append(actual_time)
                predicted_times.append(predicted_time)

                results.append((start_lat, start_long, end_lat, end_long, actual_time, predicted_time, accuracy))

    results_df = pd.DataFrame(results, columns=['START_LAT', 'START_LONG', 'END_LAT', 'END_LONG', 'Actual_Time_Taken', 'Predicted_Time_Taken', 'Accuracy'])
    results_df.to_csv('results.csv', index=False)

    if valid_rows > 0:
        overall_accuracy = total_accuracy / valid_rows
        f1 = calculate_f1_score(actual_times, predicted_times)

        accuracy_file = 'model_accuracy.txt'
        with open(accuracy_file, 'w') as f:
            f.write(f"Overall model accuracy: {overall_accuracy:.2f}%\n")
            f.write(f"F1-Score: {f1:.2f}\n")

        print(f"Overall accuracy and F1-Score saved to {accuracy_file}")
    else:
        print("No valid rows to calculate overall accuracy.")


input_file = 'MainEvaluation.csv'
compare_time_taken(input_file)
