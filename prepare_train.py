import math
import pandas as pd


CSV = "./data/vic/ScatsOctober2006_converted.csv"

df = pd.read_csv(CSV, encoding="utf-8")


# 70% to 30% ratio

DAYS_IN_OCTOBER = 31

NUMBER_OF_DAYS = math.ceil(DAYS_IN_OCTOBER * 0.7)

NUMBER_OF_15_MINUTES_PER_DAY = 96

NUMBER_OF_PERIODS = NUMBER_OF_DAYS * NUMBER_OF_15_MINUTES_PER_DAY

train_df = df.iloc[:NUMBER_OF_PERIODS]

# rest use as test data
test_df = df.iloc[NUMBER_OF_PERIODS:]

# save to csv

train_df.to_csv("./data/vic/train.csv", index=False)

test_df.to_csv("./data/vic/test.csv", index=False)
