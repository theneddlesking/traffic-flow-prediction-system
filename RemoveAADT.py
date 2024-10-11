import pandas as pd


traffic_df = pd.read_csv('data/vic/Traffic_Count_Locations_with_LONG_LAT.csv')


filtered_traffic_df = traffic_df[traffic_df['AADT_ALL_VEHICLES'] != 0]


filtered_traffic_df.to_csv('data/vic/NewData/Filtered_Traffic_Count_Locations.csv', index=False)

print(f"Filtered data saved as 'Filtered_Traffic_Count_Locations.csv'. {len(filtered_traffic_df)} rows remain after filtering.")
