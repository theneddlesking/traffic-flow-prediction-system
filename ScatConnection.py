import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

traffic_df = pd.read_csv('data/vic/Traffic_Count_Locations_with_LONG_LAT.csv')
scats_df = pd.read_csv('data/vic/SCATS_SiteDefinition.csv')

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

#function to normalize a description by expanding abbreviations
def normalize_description(desc):
    desc = desc.lower().strip()
    for abbr, full in abbreviations.items():
        desc = desc.replace(f' {abbr} ', f' {full} ')
    return desc

#fuzzy matching function
def fuzzy_match_scats_to_traffic(traffic_df, scats_df, threshold=80):
    scats_df['LATITUDE'] = None
    scats_df['LONGITUDE'] = None

    # Combine TFM_DESC and SITE_DESC for a more complete description
    traffic_df['FULL_DESC'] = traffic_df['TFM_DESC'].fillna('') + " " + traffic_df['SITE_DESC'].fillna('')

    #Init tqdm
    for scats_index, scats_row in tqdm(scats_df.iterrows(), total=len(scats_df), desc="Matching SCATS to Traffic"):
        scats_desc = normalize_description(scats_row['LOCATION_DESCRIPTION'])
        best_score = 0
        best_match = None

        # Loop through traffic data to find the best fuzzy match
        for index, row in traffic_df.iterrows():
            site_desc = normalize_description(row['FULL_DESC'])
            score = fuzz.partial_ratio(scats_desc, site_desc)  #fuzzy match score

            if score > best_score:
                best_score = score
                best_match = row

        
        if best_score >= threshold and best_match is not None:
            scats_df.at[scats_index, 'LATITUDE'] = best_match['LATITUDE']
            scats_df.at[scats_index, 'LONGITUDE'] = best_match['LONGITUDE']

    return scats_df

#optional
def calculate_zero_aadt_percentage(traffic_df):
    total_rows = len(traffic_df)
    zero_aadt_rows = len(traffic_df[traffic_df['AADT_ALL_VEHICLES'] == 0])
    percentage_zero_aadt = (zero_aadt_rows / total_rows) * 100
    return percentage_zero_aadt



#updated_scats_df = fuzzy_match_scats_to_traffic(traffic_df, scats_df, threshold=80)

#zero AADT_ALL_VEHICLES amount
zero_aadt_percentage = calculate_zero_aadt_percentage(traffic_df)
print(f"Percentage of rows with AADT_ALL_VEHICLES = 0: {zero_aadt_percentage:.2f}%")


#updated_scats_df.to_csv('ScatsLatLong.csv', index=False)

#print("Saved as 'ScatsLatLong.csv'")
