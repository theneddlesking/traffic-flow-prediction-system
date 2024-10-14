import csv
import requests

# Your Google Maps or OpenStreetMap API key idk
API_KEY = 'API_KEY'

def get_travel_time(start_lat, start_long, end_lat, end_long, departure_time):
    #Google Maps
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_long}&destination={end_lat},{end_long}&departure_time={departure_time}&key={API_KEY}"


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

def main(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['TIME_TAKEN']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            start_lat = row['START_LAT']
            start_long = row['START_LONG']
            end_lat = row['END_LAT']
            end_long = row['END_LONG']
            departure_time = row['TIME_OF_DEPARTURE']  #Unix timestamp format maybe hopefully

            #Fetch travel time
            travel_time = get_travel_time(start_lat, start_long, end_lat, end_long, departure_time)
            
            if travel_time:
                row['TIME_TAKEN'] = travel_time
            else:
                row['TIME_TAKEN'] = 'Error'

            writer.writerow(row)

if __name__ == '__main__':
    input_csv = 'ScatsOctober2006.csv' 
    output_csv = 'output_file.csv'
    main(input_csv, output_csv)
