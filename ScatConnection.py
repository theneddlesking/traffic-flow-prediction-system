import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

#Values
traffic_sample_size=1000
scats_sample_size=1000
threshold=80

#Load the datasets
traffic_df = pd.read_csv('Filtered_Traffic_Count_Locations.csv')
scats_df = pd.read_csv('ScatsLatLong.csv')
laneNum_df = pd.read_csv('Road_Width_and_Number_of_Lanes.csv')

abbreviations = { 
    'nr': 'near',
    'rd': 'road',
    'hw': 'highway',
    'st': 'street',
    'av': 'avenue',
    'jct': 'junction',
    'fwy': 'freeway',
    'rbt': 'roundabout',
    'pl': 'place',
    'crt': 'court',
    'dr': 'drive',
    'bd': '',  
}

def normalize_description(desc):
    desc = desc.lower().strip()
    for abbr, full in abbreviations.items():
        desc = desc.replace(f' {abbr} ', f' {full} ')
    return desc

# Function to match SCATS to traffic data and extract lane numbers
def fuzzy_match_scats_to_traffic_subset(traffic_df, scats_df, laneNum_df, threshold=80):
    # Select samples from traffic and SCATS data for testing
    traffic_sample = traffic_df.sample(n=traffic_sample_size, random_state=1)
    scats_sample = scats_df.sample(n=scats_sample_size, random_state=1)
    output_rows = []

    # Create a combined description column
    traffic_sample['FULL_DESC'] = traffic_sample['TFM_DESC'].fillna('') + " " + traffic_sample['SITE_DESC'].fillna('')

    for scats_index, scats_row in tqdm(scats_sample.iterrows(), total=len(scats_sample), desc="Matching SCATS to Traffic Subset"):
        scats_desc = normalize_description(scats_row['LOCATION_DESCRIPTION'])
        best_score = 0
        best_match = None

        for index, row in traffic_sample.iterrows():
            site_desc = normalize_description(row['FULL_DESC'])
            score = fuzz.partial_ratio(scats_desc, site_desc)  # Fuzzy match score

            if score > best_score:
                best_score = score
                best_match = row

        number_of_lanes = 'N/A'
        if best_match is not None:
            road_nbr = best_match['ROAD_NBR']
            lane_match = laneNum_df[laneNum_df['ROAD_NBR'] == road_nbr]
            if not lane_match.empty:
                number_of_lanes = lane_match.iloc[0]['NUMBER_OF_TRAFFIC_LANES']

       
        if best_score >= threshold and best_match is not None:
            output_row = {
                'LONG': best_match['LONGITUDE'],
                'LAT': best_match['LATITUDE'],
                'SCATS_ID': scats_row['SITE_NUMBER'],
                'NAME': scats_row['LOCATION_DESCRIPTION'],
                'TYPE_OF_ROAD': best_match['TFM_TYP_DE'],
                'SPEED_LIMIT': 'N/A',
                'NUMBER_OF_LANES': number_of_lanes,
                'AADT': best_match['AADT_ALL_VEHICLES'],
                'ROAD_NUMBER': best_match['ROAD_NBR'],
            }
            output_rows.append(output_row)

    return output_rows

matched_data_subset = fuzzy_match_scats_to_traffic_subset(traffic_df, scats_df, laneNum_df, threshold=80)

matched_df_subset = pd.DataFrame(matched_data_subset)
matched_df_subset.to_csv('TestMainCSV.csv', index=False)

print("Saved as 'TestMainCSV.csv'")
