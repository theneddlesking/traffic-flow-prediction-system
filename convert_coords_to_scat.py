import geojson
import pandas as pd


SPEED_CSV = "./data/vic/speed_limits.csv"

# only take the first 1000 rows

speed_limit_df = pd.read_csv(SPEED_CSV, nrows=1000)

print(speed_limit_df.head())

cols = speed_limit_df.columns

TRAFFIC_COUNTS_CSV = "./data/vic/Traffic_Count_Locations_with_LONG_LAT.csv"

traffic_counts_df = pd.read_csv(TRAFFIC_COUNTS_CSV)

# only take cols LONGITUDE, LATITUDE, TFM_DESC

traffic_counts_df = traffic_counts_df[["LONGITUDE", "LATITUDE", "TFM_DESC"]]


coords_df = speed_limit_df[["coordinates"]]

# take first row

coords = coords_df.iloc[0]["coordinates"]

# convert to list

coords = geojson.loads(coords)

# pretty print the first row

print(geojson.dumps(coords, indent=4))
