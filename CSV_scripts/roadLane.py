import pandas as pd

# Load the datasets
improved_csv_df = pd.read_csv('ImprovedCSV.csv')
laneNum_df = pd.read_csv('Road_Width_and_Number_of_Lanes.csv')

# Perform the merge to get 'NUMBER_OF_TRAFFIC_LANES' from 'laneNum_df' to 'improved_csv_df'
# Merging on 'ROAD_NUMBER' from ImprovedCSV with 'ROAD_NBR' from laneNum_df
improved_csv_df = pd.merge(
    improved_csv_df, 
    laneNum_df[['ROAD_NBR', 'NUMBER_OF_TRAFFIC_LANES']], 
    left_on='ROAD_NUMBER', 
    right_on='ROAD_NBR', 
    how='left'
)

# Drop the extra 'ROAD_NBR' column after the merge
improved_csv_df = improved_csv_df.drop(columns=['ROAD_NBR'])

# Save the result to a new CSV file
improved_csv_df.to_csv('FinalImprovedCSV.csv', index=False)

print("Final CSV saved as 'FinalImprovedCSV.csv'")
