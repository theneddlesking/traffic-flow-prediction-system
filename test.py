import pandas as pd
from data_loader import DataLoader
from processing_step import ProcessingSteps

CSV = "./data/vic/ScatsOctober2006.csv"

data_loader = DataLoader(
    CSV,
    "location",
    [
        # rename columns
        ProcessingSteps.rename_columns(
            {
                "LOCATION": "location",
            }
        ),
        # drop duplicates
        ProcessingSteps.drop_duplicates(),
        ProcessingSteps.drop_columns(
            [
                "SITE_NUMBER",
                "CD_MELWAY",
                "NB_LATITUDE",
                "NB_LONGITUDE",
                "HF_VICROADS_INTERNAL",
                "VR_INTERNAL_STAT",
                "VR_INTERNAL_LOCATION",
                "NB_TYPE_SURVEY",
            ]
        ),
        ProcessingSteps.filter_rows(
            lambda df: df["location"] != "AUBURN_RD N of BURWOOD_RD"
        ),
        # filter to most common date
        ProcessingSteps.filter_rows(lambda df: df["DATE"] == df["DATE"].mode()[0]),
    ],
)


print(data_loader.get_real_time_sources(data_loader.pre_processed_df, 12, 96))

# check dates

print(data_loader.pre_processed_df.head())
