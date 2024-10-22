import pandas as pd
from data_loader import DataLoader
from processing_step import ProcessingSteps

CSV = "./data/vic/ScatsOctober2006.csv"


def most_common_date(df: pd.DataFrame) -> str:
    """Get the most common date in the data frame."""
    modes = df["DATE"].mode()

    # take the second earliest date because we also want the day before
    return modes[1]


def day_before(date: str) -> str:
    """Get the day before the given date."""
    time = pd.Timestamp(date)

    timestamp = time - pd.Timedelta(days=1)

    # convert to string
    date_str = timestamp.strftime("%m/%d/%y")

    # drop leading 0 on day

    # eg. 10/04/06 -> 10/4/06

    if date_str[3] == "0":
        date_str = date_str[:3] + date_str[4:]

    return date_str


data_loader = DataLoader(
    CSV,
    # arbitrary target
    "V00",
    [
        # rename columns
        ProcessingSteps.rename_columns(
            {
                "LOCATION": "location",
            }
        ),
        # filter out bad location
        ProcessingSteps.filter_rows(
            lambda df: df["location"] != "AUBURN_RD N of BURWOOD_RD"
        ),
        ProcessingSteps.filter_rows(
            lambda df: df["location"] != "HIGH_ST NE of CHARLES_ST"
        ),
        # drop duplicates
        ProcessingSteps.drop_duplicates(),
        # remove unneeded columns
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
        # filter to most common date or the day before
        ProcessingSteps.filter_rows(
            lambda df: df["DATE"].isin(
                [most_common_date(df), day_before(most_common_date(df))]
            ),
        ),
    ],
)

sources = data_loader.get_real_time_sources(data_loader.pre_processed_df, 12, 15)
