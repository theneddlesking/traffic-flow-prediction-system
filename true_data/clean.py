import pandas as pd

def clean_routes_data(input_file, output_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Filter out rows where Time_Taken is 'Too close - Skipped' or 'Error'
    df_cleaned = df[~df['Time_Taken'].isin(['Too close - Skipped', 'Error'])]
    
    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
# Example usage:
input_file = 'trueData.csv'
output_file = 'cleanTrueData.csv'
clean_routes_data(input_file, output_file)
