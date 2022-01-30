from typing import Dict

import numpy as np
import pandas as pd


def decode_val(data_to_clean, column, vals: Dict):
    """

    :param data_to_clean:
    :param column:
    :param vals:
    :return:
    """
    data_to_clean = data_to_clean.copy()
    data_to_clean[column] = data_to_clean[column].apply(lambda x: vals.get(x, np.nan))
    return data_to_clean


def decode_demo_values(data_to_clean: pd.DataFrame, decode_demo_info: Dict) -> pd.DataFrame:
    """

    :param data_to_clean:
    :param decode_demo_info:
    :return:
    """
    data_to_clean = data_to_clean.copy()
    for key, val in decode_demo_info.items():
        data_to_clean = decode_val(data_to_clean, key, val)
        data_to_clean = data_to_clean[~data_to_clean[key].isnull()]

    return data_to_clean
