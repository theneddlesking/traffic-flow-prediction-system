import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

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


def fuzzy_match_scats_to_traffic(traffic_df, scats_df, laneNum_df, threshold=80):
    output_rows = []

    for index, row in tqdm(traffic_df.iterrows(), total=len(traffic_df), desc="Matching Traffic Data"):
        road_nbr = row['ROAD_NBR']
        declared_road = row['DECLARED_ROAD']
        site_desc = normalize_description(row['SITE_DESC'])

        #look for matching rows in the Road Width data
        lane_match = laneNum_df[(laneNum_df['ROAD_NBR'] == road_nbr) & (laneNum_df['ROAD_NAME'].str.contains(declared_road, case=False, na=False))]
        number_of_lanes = lane_match.iloc[0]['NUMBER_OF_TRAFFIC_LANES'] if not lane_match.empty else 'N/A'

        #look for matching rows in the SCATS data
        best_score = 0
        best_match = None
        scats_id = 'N/A'

        for scats_index, scats_row in scats_df.iterrows():
            scats_desc = normalize_description(scats_row['LOCATION_DESCRIPTION'])
            scats_parts = scats_desc.split('/')

            #checking if both parts match the traffic SITE_DESC
            score_parts = [fuzz.partial_ratio(part.strip(), site_desc) for part in scats_parts]
            min_score = min(score_parts) if score_parts else 0

            if min_score > best_score:
                best_score = min_score
                best_match = scats_row

        if best_score >= threshold and best_match is not None:
            scats_id = best_match['SITE_NUMBER']

        output_row = {
            'LONG': row['LONGITUDE'],
            'LAT': row['LATITUDE'],
            'SCATS_ID': scats_id,
            'NAME': row['DECLARED_ROAD'],
            'SITE_DESC': row['SITE_DESC'],
            'TYPE_OF_ROAD': row['TFM_TYP_DE'],
            'NUMBER_OF_LANES': number_of_lanes,
            'AADT': row['AADT_ALL_VEHICLES'],
            'ROAD_NUMBER': road_nbr,
            'SPEED_LIMIT': 'N/A',
        }
        output_rows.append(output_row)

    return output_rows

matched_data = fuzzy_match_scats_to_traffic(traffic_df, scats_df, laneNum_df, threshold=60)

matched_df = pd.DataFrame(matched_data)
matched_df.to_csv('ImprovedMainCSV.csv', index=False)

print("Saved as 'ImprovedMainCSV.csv'")
