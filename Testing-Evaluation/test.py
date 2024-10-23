import pandas as pd
import requests
import sqlite3

db_path = "site.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to test the API call
def test_api_call(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print(f"API call failed with status code: {response.status_code}")

# Function to get the location_id from latitude and longitude
def get_location_id(lat, long):
    cursor.execute("SELECT id FROM locations WHERE lat = ? AND long = ?", (lat, long))
    result = cursor.fetchone()
    return result[0] if result else None

# Function to get time prediction from the model
def get_time_from_model(start_location_id, end_location_id, time_of_day):
    url = f"http://localhost:8000/routing/route?start_location_id={start_location_id}&end_location_id={end_location_id}&time_of_day={time_of_day}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"API Response Data: {data}")  # Debugging print
        return data.get("hours_taken")
    else:
        print(f"API call failed with status code: {response.status_code}")
    return None

# Function to calculate accuracy of prediction
def calculate_accuracy(predicted_time, actual_time):
    if actual_time == 0:
        return 0
    return 100 - abs((predicted_time - actual_time) / actual_time * 100)

# Function to compare the time taken between actual data and predictions
def compare_time_taken(input_file):
    df = pd.read_csv(input_file)

    results = []
    
    total_accuracy = 0
    valid_rows = 0 
    # Iterate over each row in the true data CSV and compare them against basic_predictions

    for index, row in df.iterrows():
        start_lat = row['START_LAT']
        start_long = row['START_LONG']
        end_lat = row['END_LAT']
        end_long = row['END_LONG']
        actual_time = row['Time_Taken']
        time_of_day = row['Time']

        start_location_id = get_location_id(start_lat, start_long)
        end_location_id = get_location_id(end_lat, end_long)
        
        if start_location_id and end_location_id:
            predicted_time = get_time_from_model(start_location_id, end_location_id, time_of_day)
            
            if predicted_time is not None:
                accuracy = calculate_accuracy(predicted_time, actual_time)

                total_accuracy += accuracy
                valid_rows += 1

                results.append((start_lat, start_long, end_lat, end_long, actual_time, predicted_time, accuracy))

    # Save results to CSV
    results_df = pd.DataFrame(results, columns=['START_LAT', 'START_LONG', 'END_LAT', 'END_LONG', 'Actual_Time_Taken', 'Predicted_Time_Taken', 'Accuracy'])
    results_df.to_csv('results.csv', index=False)

    # Save overall accuracy to a text file
    if valid_rows > 0:
        overall_accuracy = total_accuracy / valid_rows
        accuracy_file = 'model_accuracy.txt'
        with open(accuracy_file, 'w') as f:
            f.write(f"Overall model accuracy: {overall_accuracy:.2f}%\n")
        print(f"Overall accuracy saved to {accuracy_file}")
    else:
        print("No valid rows to calculate overall accuracy.")

# Run the comparison with the provided CSV file
input_file = 'cleanTrueData.csv'
compare_time_taken(input_file)
