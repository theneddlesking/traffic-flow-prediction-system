import pandas as pd


CSV = "./data/vic/ScatsOctober2006_converted.csv"

df = pd.read_csv(CSV, encoding="utf-8")

# shuffle it

df = df.sample(frac=1).reset_index(drop=True)

# take 70% as train
train_df = df[: int(len(df) * 0.7)]

# take 30% as test
test_section = int(len(df) * 0.7)
test_df = df[test_section:]

# save to csv
train_df.to_csv("./data/vic/train.csv", index=False)
test_df.to_csv("./data/vic/test.csv", index=False)
