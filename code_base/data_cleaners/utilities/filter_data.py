from typing import List

import pandas as pd


def filter_columns(data_to_clean: pd.DataFrame, filt_cols: List) -> pd.DataFrame:
    """

    :param data_to_clean:
    :param filt_cols:
    :return:
    """
    mask = ~data_to_clean.columns.isin(filt_cols)
    data_to_clean.drop(data_to_clean.columns[mask],
                       axis=1,
                       inplace=True)

    return data_to_clean


def filter_rows_containing_string(data_to_clean: pd.DataFrame, column_name: str, filter_string: str) -> pd.DataFrame:
    """

    :param data_to_clean:
    :param column_name:
    :param filter_string:
    :return:
    """

    mask = ~data_to_clean[column_name].str.contains(filter_string)
    data_to_clean.drop(data_to_clean[mask].index, inplace=True)

    return data_to_clean
