from typing import Union, List

import pandas as pd


def replace_symbols(data_to_clean, symbol_to_replace: str, replace_with: Union[str, float], apply_to_cols: List) -> pd.DataFrame:
    """
    Method replaces symbols related to data cleaning, e.g. replace ("P") values put next to mortality values.
    to signify "preliminary data" with nothing ("").

    :param symbol_to_replace: Symbol that needs to be replaced.
    :param replace_with: The symbol to be replaced with.
    :param apply_to_cols: List of columns for which the replace function is applicable.
    :return: The method does not return data. It manipulates the existing dataframe within the class instance.
    """
    data_to_clean[apply_to_cols] = data_to_clean[apply_to_cols].replace(symbol_to_replace, replace_with, regex=True)

    return data_to_clean


def strip_spaces(strip_spaces_from: List) -> List:
    return [string.strip() for string in strip_spaces_from]
