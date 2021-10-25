from typing import List, Dict, Union

import pandas as pd


def split_columns_by_data(data_to_clean: pd.DataFrame,
                          split_from: str,
                          split_into: List,
                          separator: str) -> pd.DataFrame:
    """

    :param data_to_clean:
    :param split_from:
    :param split_into:
    :param separator:
    :return:
    """
    col_ind = data_to_clean.columns.get_loc(split_from)
    data_to_clean[split_into] = data_to_clean.iloc[:, col_ind].str.split(pat=separator, expand=True)
    data_to_clean.drop(split_from, axis=1, inplace=True)

    return data_to_clean


def convert_cols_to_rows(data_to_clean: pd.DataFrame, retain_columns, cols_to_rows, col_values_name) -> pd.DataFrame:
    """

    :param data_to_clean:
    :param retain_columns:
    :param cols_to_rows:
    :param col_values_name:
    :return:
    """

    data_to_clean = data_to_clean.melt(id_vars=retain_columns, var_name=cols_to_rows, value_name=col_values_name)

    return data_to_clean


def convert_rows_to_cols(data_to_clean, index_cols, target_row_col, fill_with_data):
    """

    :param data_to_clean:
    :param index_cols:
    :param target_row_col:
    :param fill_with_data:
    :return:
    """
    data_to_clean = data_to_clean.pivot(index=index_cols,
                                        columns=target_row_col,
                                        values=fill_with_data)

    return data_to_clean
