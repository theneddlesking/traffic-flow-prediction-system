import pandas as pd
from tqdm import tqdm
from rapidfuzz import fuzz

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

def fuzzy_match_scats_to_traffic(traffic_df, scats_df, threshold=80):
    output_rows = []

    for index, row in tqdm(traffic_df.iterrows(), total=len(traffic_df), desc="Matching Traffic Data"):
        road_nbr = row['ROAD_NBR']
        declared_road = row['DECLARED_ROAD']
        site_desc = normalize_description(row['SITE_DESC'])

        best_score = 0
        best_match = None
        scats_id = 'NaN'
        name = row['SITE_DESC']  # name default to SITE_DESC from traffic data

        for scats_index, scats_row in scats_df.iterrows():
            scats_desc = normalize_description(scats_row['LOCATION_DESCRIPTION'])
            scats_parts = scats_desc.split('/')

            #check if both parts match the traffic SITE_DESC using fuzzy matching
            score_parts = [fuzz.partial_ratio(part.strip(), site_desc) for part in scats_parts]
            min_score = min(score_parts) if score_parts else 0

            if min_score > best_score:
                best_score = min_score
                best_match = scats_row

        if best_score >= threshold and best_match is not None:
            scats_id = best_match['SITE_NUMBER']
            name = best_match['LOCATION_DESCRIPTION']  #use LOCATION_DESCRIPTION as the name if SCATS is matched

        #save the output row without the number of lanes
        output_row = {
            'LONG': row['LONGITUDE'],
            'LAT': row['LATITUDE'],
            'SCATS_ID': scats_id,
            'NAME': name,  #name is based on SCATS or fallback to SITE_DESC
            'SITE_DESC': row['SITE_DESC'],
            'TYPE_OF_ROAD': row['TFM_TYP_DE'],
            'AADT': row['AADT_ALL_VEHICLES'],
            'ROAD_NUMBER': road_nbr,
            'SPEED_LIMIT': 'NaN',
        }
        output_rows.append(output_row)

    return output_rows

def add_lane_data(improved_csv_df, laneNum_df):
    merged_df = pd.merge(improved_csv_df, laneNum_df[['ROAD_NBR', 'NUMBER_OF_TRAFFIC_LANES']], 
                         left_on='ROAD_NUMBER', right_on='ROAD_NBR', how='left')

    merged_df = merged_df.drop(columns=['ROAD_NBR'])

    return merged_df

matched_data = fuzzy_match_scats_to_traffic(traffic_df, scats_df, threshold=80)

improved_csv_df = pd.DataFrame(matched_data)

final_df = add_lane_data(improved_csv_df, laneNum_df)

final_df.to_csv('ImprovedMainCSV.csv', index=False)

print("Saved as 'ImprovedMainCSV.csv'")
