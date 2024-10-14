import csv
import requests
#Open Street Map
def get_osrm_travel_time(start_lat, start_long, end_lat, end_long):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_long},{start_lat};{end_long},{end_lat}?overview=false"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        duration = data['routes'][0]['duration'] / 60  # Convert seconds to minutes
        return f"{int(duration)} minutes"
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

            #Fetch travel time
            travel_time = get_osrm_travel_time(start_lat, start_long, end_lat, end_long)
            
            if travel_time:
                row['TIME_TAKEN'] = travel_time
            else:
                row['TIME_TAKEN'] = 'Error'

            writer.writerow(row)

if __name__ == '__main__':
    input_csv = 'ScatsOctober2006.csv' 
    output_csv = 'output_file.csv'
    main(input_csv, output_csv)
