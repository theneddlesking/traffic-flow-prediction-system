import pandas as pd
from tqdm import tqdm
from rapidfuzz import fuzz

traffic_df = pd.read_csv('Filtered_Traffic_Count_Locations.csv')
scats_df = pd.read_csv('ScatsLatLong.csv')
laneNum_df = pd.read_csv('Road_Width_and_Number_of_Lanes.csv')

#select subnet amount for testing
#traffic_df = traffic_df.sample(n=5000, random_state=1)

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

        best_score = 0
        best_match = None
        scats_id = 'N/A'
        name = row['SITE_DESC']  #Default to traffic SITE_DESC

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
            name = best_match['LOCATION_DESCRIPTION']  #use scats name if matched

        #match the lane number
        if road_nbr == 9999:  #Match based on name instead of road number (9999 is null)
            lane_match = laneNum_df[laneNum_df['ROAD_NAME'].str.contains(declared_road, case=False, na=False, regex=False)]
        else:  #Match based on road number (if not 9999)
            lane_match = laneNum_df[laneNum_df['ROAD_NBR'] == road_nbr]
        
        number_of_lanes = lane_match.iloc[0]['NUMBER_OF_TRAFFIC_LANES'] if not lane_match.empty else 'N/A'

        # Only save the row if either SCATS ID or number of lanes are found
        if scats_id != 'N/A' or number_of_lanes != 'N/A':
            output_row = {
                'LONG': row['LONGITUDE'],
                'LAT': row['LATITUDE'],
                'SCATS_ID': scats_id,
                'NAME': name,  #set the name based on scats or fallback to SITE_DESC
                'SITE_DESC': row['SITE_DESC'],
                'TYPE_OF_ROAD': row['TFM_TYP_DE'],
                'NUMBER_OF_LANES': number_of_lanes,
                'AADT': row['AADT_ALL_VEHICLES'],
                'ROAD_NUMBER': road_nbr,
                'SPEED_LIMIT': 'N/A', #plan: if speed limit is not found and no scats are found drop the row
            }
            output_rows.append(output_row)

    return output_rows

matched_data = fuzzy_match_scats_to_traffic(traffic_df, scats_df, laneNum_df, threshold=80)

matched_df = pd.DataFrame(matched_data)
matched_df.to_csv('MainCSV.csv', index=False)

print("Saved as 'MainCSV.csv'")
