from typing import Callable, List

import pandas as pd


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
