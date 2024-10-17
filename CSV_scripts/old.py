import pandas as pd

# Function to match SCATS site numbers by splitting SCATS descriptions and looking for all words in Traffic site descriptions
def improved_match_scats_to_traffic(traffic_df, scats_df):
    # Initialize a new column in traffic_df for SCATS numbers
    traffic_df['SCATS_SITE_NUMBER_SUBSTRING'] = None


    # Iterate through traffic data and match based on split SCATS descriptions
    for index, row in traffic_df.iterrows():
        site_desc = row['SITE_DESC'].strip().lower()
        for scats_index, scats_row in scats_df.iterrows():
            scats_desc = scats_row['LOCATION_DESCRIPTION'].strip().lower()
            # Split the SCATS description by '/' and check if all parts are present in the traffic site description
            scats_parts = scats_desc.split('/')
            if all(part.strip() in site_desc for part in scats_parts):
                # If a match is found, add the SCATS site number
                traffic_df.at[index, 'SCATS_SITE_NUMBER_SUBSTRING'] = scats_row['SITE_NUMBER']
                break  # Once a match is found, move to the next traffic site

    return traffic_df

# Load the CSV files (assuming you already have them in the current working directory)
traffic_df = pd.read_csv('Traffic_Count_Locations_with_LONG_LAT.csv')
scats_df = pd.read_csv('SCATS_SiteDefinition.csv')

# Example usage: Apply the function to a subset of the data
updated_traffic_df = improved_match_scats_to_traffic(traffic_df, scats_df)

# Save the updated DataFrame to a CSV file
updated_traffic_df.to_csv('Improved_Updated_Traffic_Count_Locations.csv', index=False)

print("The updated CSV file has been saved as 'Improved_Updated_Traffic_Count_Locations.csv'")
