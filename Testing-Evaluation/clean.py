import pandas as pd

def filter_monday(input_file, output_file):
    df = pd.read_csv(input_file)

    df_filtered = df[df['Day'] == 'Monday']

    df_filtered.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

input_file = 'cleanTrueData.csv'
output_file = 'cleanTrueData_Monday.csv'
filter_monday(input_file, output_file)
