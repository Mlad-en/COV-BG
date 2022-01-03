from typing import List

import pandas as pd
from numpy import ndarray, unique

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_calculations.utils.prediction_utils import (get_prev_years_indices,
                                                                get_timeframe_count,
                                                                get_analyzed_year_indices,
                                                                generate_predictors,
                                                                predict_baseline,
                                                                get_mortality_eea_info,
                                                                generate_std,
                                                                is_significant)


def predict(all_mort: ndarray) -> tuple:
    """

    :param all_mort: Receives a ndarray of size (n x 3), where  the columns are:
    1. Year
    2. Week
    3. Mortality
    :return: Returns calculations for:
     1. Expected Mortality (predicted based on previous 5 years)
     2. Actual Mortality
     3. Excess Mortality (diff between actual and expected mortality)
     4. Excess Mortality Standard Deviation
    """

    prev_years = get_prev_years_indices(all_mort)
    time_frame_pys = get_timeframe_count(all_mort, prev_years)

    analyzed_year = get_analyzed_year_indices(all_mort)
    time_frame_ay = get_timeframe_count(all_mort, analyzed_year)

    assert time_frame_pys == time_frame_ay

    train_on = generate_predictors(all_mort, prev_years, time_frame_pys)
    predict_for = generate_predictors(all_mort, analyzed_year, time_frame_ay)

    baseline = predict_baseline(train_on, all_mort[prev_years, 2], predict_for)

    # Excess mortality
    total_excess, sum_expected, sum_actual = get_mortality_eea_info(all_mort, analyzed_year, baseline)

    # Manually Fit Data
    total_excess_std = generate_std(all_mort, prev_years, train_on, predict_for, time_frame_pys)

    return total_excess, sum_expected, sum_actual, total_excess_std


def add_significance(df: pd.dataframe) -> pd.DataFrame:
    df[COL_HEAD.Z_SCORE] = df.apply(lambda x: x[COL_HEAD.EXCESS_MORTALITY] / x[COL_HEAD.STANDARD_DEVIATION], axis=1)
    df[COL_HEAD.IS_SIGNIFICANT] = df.apply(lambda x: is_significant(x[COL_HEAD.Z_SCORE]), axis=1)

    return df


def get_predicted_mortality(df: pd.DataFrame, analyze_years: List) -> pd.DataFrame:

    df = df.melt(id_vars=[COL_HEAD.LOCATION, COL_HEAD.WEEK, COL_HEAD.SEX],
                 value_vars=analyze_years,
                 var_name=COL_HEAD.YEAR,
                 value_name=COL_HEAD.MORTALITY)
    df[COL_HEAD.YEAR] = df[COL_HEAD.YEAR].astype(int)

    countries = unique(df[COL_HEAD.LOCATION])
    sexes = unique(df[COL_HEAD.SEX])

    const_df = {
        COL_HEAD.LOCATION: [],
        COL_HEAD.SEX: [],
        COL_HEAD.MEAN_OR_EXPECTED_MORTALITY: [],
        COL_HEAD.MORTALITY: [],
        COL_HEAD.EXCESS_MORTALITY: [],
        COL_HEAD.STANDARD_DEVIATION: [],
    }

    for _, country in enumerate(countries):
        for _, sex in enumerate(sexes):

            X = df[(df[COL_HEAD.LOCATION] == country) & (df[COL_HEAD.SEX] == sex)][
                [COL_HEAD.YEAR, COL_HEAD.WEEK, COL_HEAD.MORTALITY]
            ].values
            X = X.astype(int)

            total_excess, sum_expected, sum_actual, total_excess_std = predict(X)

            const_df[COL_HEAD.LOCATION].append(country)
            const_df[COL_HEAD.SEX].append(sex)
            const_df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY].append(sum_expected)
            const_df[COL_HEAD.MORTALITY].append(sum_actual)
            const_df[COL_HEAD.EXCESS_MORTALITY].append(total_excess)
            const_df[COL_HEAD.STANDARD_DEVIATION].append(total_excess_std)

    return pd.DataFrame(const_df)


