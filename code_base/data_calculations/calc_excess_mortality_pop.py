from typing import List

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class CalculateEurostatExcessMortalityToPopulation:

    @staticmethod
    def _calc_pop_to_excess_mortality(mort_df, pop_df, merge_on_cols):
        """

        :return:
        """
        mort_df = mort_df.merge(pop_df, on=merge_on_cols)

        mort_df[COL_HEAD.EXCESS_MORTALITY_PER_100_000] = mort_df.apply(
            lambda x: x[COL_HEAD.EXCESS_MORTALITY_MEAN] / x[COL_HEAD.POPULATION] * 100_000,
            axis=1).round(1)

        mort_df[COL_HEAD.EXCESS_MORTALITY_PER_100_000_FLUCTUATION] = mort_df.apply(
            lambda x:
            abs(
                (
                        (x[COL_HEAD.EXCESS_MORTALITY_MEAN] + x[COL_HEAD.CONFIDENCE_INTERVAL])
                        / x[COL_HEAD.POPULATION] * 100_000
                )
                - x[COL_HEAD.EXCESS_MORTALITY_PER_100_000]
            ),
            axis=1).round(1)

        return mort_df

    @staticmethod
    def _concat_column_vals(df: pd.DataFrame, main_col, additional_col, brackets: List):
        return df[main_col].map(str) + brackets[0] + df[additional_col].map(str) + brackets[1]

    def _add_formatted_cols(self, df: pd.DataFrame):
        per_100_000 = COL_HEAD.EXCESS_MORTALITY_PER_100_000
        fluctuation = COL_HEAD.EXCESS_MORTALITY_PER_100_000_FLUCTUATION
        decorated = COL_HEAD.EXCESS_MORTALITY_PER_100_000_DECORATED

        df[decorated] = self._concat_column_vals(df, per_100_000, fluctuation, [' (±', ')'])
        return df

    def calculate_excess_mortality(self, mort_df: pd.DataFrame, pop_df: pd.DataFrame, merge_on_cols: List) -> pd.DataFrame:
        comb_df = self._calc_pop_to_excess_mortality(mort_df, pop_df, merge_on_cols)
        comb_df = self._add_formatted_cols(comb_df)

        return comb_df