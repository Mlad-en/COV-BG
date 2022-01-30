from math import sqrt
from typing import List

import pandas as pd
from numpy import ndarray, unique, nan

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_calculations.utils.prediction_utils import (get_prev_years_indices,
                                                                get_timeframe_count,
                                                                get_analyzed_year_indices,
                                                                generate_predictors,
                                                                predict_baseline,
                                                                get_mortality_eea_info,
                                                                generate_std,
                                                                is_significant)


class CalculateExcessMortalityPredicted:

    def get_const_df(self, add_age: bool, add_week: bool):

        dct = {
                COL_HEAD.LOCATION: [],
                COL_HEAD.SEX: [],
                COL_HEAD.MEAN_OR_EXPECTED_MORTALITY: [],
                COL_HEAD.MORTALITY: [],
                COL_HEAD.EXCESS_MORTALITY_BASE: [],
                COL_HEAD.STANDARD_DEVIATION: [],
            }

        if add_week:
            dct[COL_HEAD.WEEK] = []

        if add_age:
            dct[COL_HEAD.AGE] = []

        return dct

    @staticmethod
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

        # Generate Excess mortality information
        total_excess, sum_expected, sum_actual = get_mortality_eea_info(all_mort, analyzed_year, baseline)

        # Generate Standard Deviation for model
        total_excess_std = generate_std(all_mort, prev_years, train_on, predict_for, time_frame_pys)

        return total_excess, sum_expected, sum_actual, total_excess_std

    def get_predicted_ls_mortality(self, df: pd.DataFrame):

        countries = unique(df[COL_HEAD.LOCATION])
        sexes = unique(df[COL_HEAD.SEX])

        const_df = self.get_const_df(False, False)

        for _, country in enumerate(countries):
            for _, sex in enumerate(sexes):
                X = df[(df[COL_HEAD.LOCATION] == country) & (df[COL_HEAD.SEX] == sex)][
                    [COL_HEAD.YEAR, COL_HEAD.WEEK, COL_HEAD.MORTALITY]
                ].values
                X = X.astype(int)

                total_excess, sum_expected, sum_actual, total_excess_std = self.predict(X)

                const_df[COL_HEAD.LOCATION].append(country)
                const_df[COL_HEAD.SEX].append(sex)
                const_df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY].append(sum_expected)
                const_df[COL_HEAD.MORTALITY].append(sum_actual)
                const_df[COL_HEAD.EXCESS_MORTALITY_BASE].append(total_excess)
                const_df[COL_HEAD.STANDARD_DEVIATION].append(total_excess_std)

        return const_df

    def get_predicted_lsa_mortality(self, df: pd.DataFrame):
        countries = unique(df[COL_HEAD.LOCATION])
        sexes = unique(df[COL_HEAD.SEX])
        ages = unique(df[COL_HEAD.AGE])

        const_df = self.get_const_df(True, False)

        for _, country in enumerate(countries):
            for _, sex in enumerate(sexes):
                for _, age in enumerate(ages):
                    X = df[(df[COL_HEAD.LOCATION] == country) & (df[COL_HEAD.SEX] == sex) & (df[COL_HEAD.AGE] == age)][
                        [COL_HEAD.YEAR, COL_HEAD.WEEK, COL_HEAD.MORTALITY]
                    ].values
                    X = X.astype(int)

                    total_excess, sum_expected, sum_actual, total_excess_std = self.predict(X)

                    const_df[COL_HEAD.LOCATION].append(country)
                    const_df[COL_HEAD.SEX].append(sex)
                    const_df[COL_HEAD.AGE].append(age)
                    const_df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY].append(sum_expected)
                    const_df[COL_HEAD.MORTALITY].append(sum_actual)
                    const_df[COL_HEAD.EXCESS_MORTALITY_BASE].append(total_excess)
                    const_df[COL_HEAD.STANDARD_DEVIATION].append(total_excess_std)

        return const_df

    def get_predicted_slw_mortality(self, df: pd.DataFrame):
        countries = unique(df[COL_HEAD.LOCATION])
        sexes = unique(df[COL_HEAD.SEX])
        weeks = unique(df[COL_HEAD.WEEK])

        const_df = self.get_const_df(False, True)

        for _, country in enumerate(countries):
            for _, sex in enumerate(sexes):
                for _, week in enumerate(weeks):
                    X = df[(df[COL_HEAD.LOCATION] == country) & (df[COL_HEAD.SEX] == sex)
                           & (df[COL_HEAD.WEEK] == week)][[COL_HEAD.YEAR, COL_HEAD.WEEK, COL_HEAD.MORTALITY]].values
                    X = X.astype(int)
                    total_excess, sum_expected, sum_actual, total_excess_std = self.predict(X)

                    const_df[COL_HEAD.LOCATION].append(country)
                    const_df[COL_HEAD.SEX].append(sex)
                    const_df[COL_HEAD.WEEK].append(week)
                    const_df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY].append(sum_expected)
                    const_df[COL_HEAD.MORTALITY].append(sum_actual)
                    const_df[COL_HEAD.EXCESS_MORTALITY_BASE].append(total_excess)
                    const_df[COL_HEAD.STANDARD_DEVIATION].append(total_excess_std)

        return const_df

    def get_predicted_mortality(self, df: pd.DataFrame, analyze_years: List, group_by: str) -> pd.DataFrame:
        """

        :param df:
        :param analyze_years:
        :param group_by: Options are 'sl', 'sla' and 'all'
        :return:
        """

        if group_by == 'sl':
            df = df.melt(id_vars=[COL_HEAD.LOCATION, COL_HEAD.WEEK, COL_HEAD.SEX],
                         value_vars=analyze_years,
                         var_name=COL_HEAD.YEAR,
                         value_name=COL_HEAD.MORTALITY)
            df[COL_HEAD.YEAR] = df[COL_HEAD.YEAR].astype(int)

            data = self.get_predicted_ls_mortality(df)
            return pd.DataFrame(data)

        if group_by == 'sla':
            df = df.melt(id_vars=[COL_HEAD.LOCATION, COL_HEAD.WEEK, COL_HEAD.SEX, COL_HEAD.AGE],
                         value_vars=analyze_years,
                         var_name=COL_HEAD.YEAR,
                         value_name=COL_HEAD.MORTALITY)
            df[COL_HEAD.YEAR] = df[COL_HEAD.YEAR].astype(int)

            data = self.get_predicted_lsa_mortality(df)
            return pd.DataFrame(data)

        if group_by == 'slw':
            df = df.melt(id_vars=[COL_HEAD.LOCATION, COL_HEAD.WEEK, COL_HEAD.SEX],
                         value_vars=analyze_years,
                         var_name=COL_HEAD.YEAR,
                         value_name=COL_HEAD.MORTALITY)
            df[COL_HEAD.YEAR] = df[COL_HEAD.YEAR].astype(int)

            data = self.get_predicted_slw_mortality(df)
            return pd.DataFrame(data)

    @staticmethod
    def _add_significance(df: pd.DataFrame) -> pd.DataFrame:
        df[COL_HEAD.Z_SCORE] = df.apply(lambda x:
                                        x[COL_HEAD.EXCESS_MORTALITY_BASE] / x[COL_HEAD.STANDARD_DEVIATION]
                                        if x[COL_HEAD.STANDARD_DEVIATION] != 0
                                        else nan,
                                        axis=1)
        df[COL_HEAD.IS_SIGNIFICANT] = df.apply(lambda x: is_significant(x[COL_HEAD.Z_SCORE]), axis=1)

        return df

    @staticmethod
    def _add_zscore_pred_int(df: pd.DataFrame):
        df[COL_HEAD.CONFIDENCE_INTERVAL] = df.apply(
            lambda x: 1.96 * x[COL_HEAD.STANDARD_DEVIATION],
            axis=1).round(1)

        return df

    @staticmethod
    def _add_mean_mort_boundaries(df: pd.DataFrame):
        """

        :return:
        """
        df[COL_HEAD.LB_MEAN_MORTALITY] = df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] - df[COL_HEAD.CONFIDENCE_INTERVAL]
        df[COL_HEAD.UB_MEAN_MORTALITY] = df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] + df[COL_HEAD.CONFIDENCE_INTERVAL]

        return df

    @staticmethod
    def _add_pscore(df: pd.DataFrame):
        """

        :param df:
        :param analyze_year:
        :return:
        """
        df[COL_HEAD.P_SCORE] = df.apply(
            lambda x:
            (
                    (x[COL_HEAD.MORTALITY] - x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY])
                    /
                    x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY]
            ) * 100
            if x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] != 0
            else 0,
            axis=1).round(1)

        df[COL_HEAD.P_SCORE_FLUCTUATION] = df.apply(
            lambda x:
            x[COL_HEAD.P_SCORE]
            -
            (
                    (
                            (x[COL_HEAD.MORTALITY] - x[COL_HEAD.UB_MEAN_MORTALITY])
                            / x[COL_HEAD.UB_MEAN_MORTALITY]
                    )
                    * 100
            )
            if x[COL_HEAD.UB_MEAN_MORTALITY] != 0
            else nan,
            axis=1).round(1)

        return df

    @staticmethod
    def _concat_column_vals(df: pd.DataFrame, main_col, additional_col, brackets: List):
        return df[main_col].map(str) + brackets[0] + df[additional_col].map(str) + brackets[1]

    def _add_formatted_cols(self, df: pd.DataFrame):
        df = df.round(1)

        df[COL_HEAD.MEAN_MORTALITY_DECORATED] = self._concat_column_vals(df,
                                                                         COL_HEAD.MEAN_OR_EXPECTED_MORTALITY,
                                                                         COL_HEAD.CONFIDENCE_INTERVAL,
                                                                         [' (±', ')'])

        df[COL_HEAD.EXCESS_MORTALITY_DECORATED] = self._concat_column_vals(df,
                                                                           COL_HEAD.EXCESS_MORTALITY_BASE,
                                                                           COL_HEAD.CONFIDENCE_INTERVAL,
                                                                           [' (±', ')'])

        df[COL_HEAD.P_SCORE_DECORATED] = self._concat_column_vals(df,
                                                                  COL_HEAD.P_SCORE,
                                                                  COL_HEAD.P_SCORE_FLUCTUATION,
                                                                  ['% (±', '%)'])

        return df

    def add_excess_mort_calcs(self, df):
        df = self._add_significance(df)
        df = self._add_zscore_pred_int(df)
        df = self._add_mean_mort_boundaries(df)
        df = self._add_pscore(df)
        df = self._add_formatted_cols(df)
        return df
