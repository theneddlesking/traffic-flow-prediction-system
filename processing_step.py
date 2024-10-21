from typing import Callable, List

import pandas as pd

from time_utils import TimeUtils


class ProcessingSteps:
    """A collection of processing steps for dataframes."""

    @staticmethod
    def drop_columns(columns: List[str]) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Drop columns from a dataframe."""
        return lambda df: df.drop(columns=columns)

    @staticmethod
    def drop_na() -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Drop rows with NA values from a dataframe."""
        return lambda df: df.dropna()

    @staticmethod
    def fill_na(value) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Fill NA values in a dataframe."""
        return lambda df: df.fillna(value)

    @staticmethod
    def rename_columns(mapping: dict) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Rename columns in a dataframe."""
        return lambda df: df.rename(columns=mapping)

    @staticmethod
    def filter_columns(columns: List[str]) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Filter columns in a dataframe."""
        return lambda df: df[columns]

    @staticmethod
    def filter_rows(
        condition: Callable[[pd.Series], pd.Series]
    ) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Filter rows in a dataframe."""
        return lambda df: df[condition(df)]

    @staticmethod
    def drop_duplicates() -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Drop duplicate rows in a dataframe."""
        return lambda df: df.drop_duplicates()

    @staticmethod
    def get_flow_per_period(period_in_minutes=15) -> pd.DataFrame:
        """Get flow per period"""

        def inner(df: pd.DataFrame):
            """Inner function to get flow per period"""
            ouput_df_rows = []

            # iter each row
            for _, row in df.iterrows():

                # get flow
                flow = row["V00":"V95"]

                # get 15 minutes
                for i in range(0, 96, 1):

                    ouput_df_rows.append(
                        {
                            "time": TimeUtils.convert_minute_index_to_str(
                                i, period_in_minutes
                            ),
                            # using iloc to get the value
                            "flow": flow.iloc[i],
                        },
                    )

            output_df = pd.DataFrame(ouput_df_rows)

            # concat the original df with the new df
            return pd.concat([df, output_df], axis=1)

        return inner

    # categorise row
    @staticmethod
    def categorise_column(column: str) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """Categorise a column in a dataframe."""
        # using pandas astype to convert to category
        return lambda df: df.astype({column: "category"})
