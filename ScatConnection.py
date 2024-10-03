import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

traffic_df = pd.read_csv('data/vic/NewData/Filtered_Traffic_Count_Locations.csv')
scats_df = pd.read_csv('data/vic/NewData/SCATS_SiteDefinition.csv')

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

# Function to perform fuzzy matching with a subset
def fuzzy_match_scats_to_traffic_subset(traffic_df, scats_df, threshold=80, traffic_sample_size=2000, scats_sample_size=2000):
    # Select a sample of rows from the original datasets for testing
    traffic_sample = traffic_df.sample(n=traffic_sample_size, random_state=1)
    scats_sample = scats_df.sample(n=scats_sample_size, random_state=1)
    output_rows = []

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


        if best_score >= threshold and best_match is not None:
            output_row = {
                'LONG': best_match['LONGITUDE'],
                'LAT': best_match['LATITUDE'],
                'SCATS_ID': scats_row['SITE_NUMBER'],
                'NAME': scats_row['LOCATION_DESCRIPTION'],
                'MAP_REFERENCE': scats_row['MAP_REFERENCE'],
                'TYPE_OF_ROAD': best_match['TFM_TYP_DE'],
                'SPEED_LIMIT': 'N/A',
                'NUMBER_OF_LANES': 'N/A',
                'AADT': best_match['AADT_ALL_VEHICLES'], 
            }
            output_rows.append(output_row)

    return output_rows

matched_data_subset = fuzzy_match_scats_to_traffic_subset(traffic_df, scats_df, threshold=80, traffic_sample_size=2000, scats_sample_size=2000)


matched_df_subset = pd.DataFrame(matched_data_subset)

matched_df_subset.to_csv('data/vic/NewData/TestMainCSV.csv', index=False)

print("Saved as 'TestMainCSV.csv'")
