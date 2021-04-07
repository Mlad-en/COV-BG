import os

import pandas as pd

from code_base.excess_mortality.folder_constants import source_cov_bg_comb, output_excess_mortality_regions
from code_base.official_bg_data.get_official_bg_data import GetOfficialBGStats
from code_base.utils.save_file_utils import SaveFile


class CovMortAttrs(SaveFile):
    """
    Class only used for the Total (all ages) age-aggregated data for Bulgarian regions.
    Cannot be used with other data sets due to limitations of data.
    """
    def __init__(self):
        self.cov_mort_file_loc = source_cov_bg_comb
        self.cov_mort_file = r"Combined_bg_Cov_19_mortality.xlsx"
        self.cov_mort = os.path.join(self.cov_mort_file_loc, self.cov_mort_file)
        self.output_loc = output_excess_mortality_regions

    @property
    def get_cov_mort_df(self):
        cov_df = pd.read_excel(self.cov_mort, sheet_name='COV-19_Mortality')
        return cov_df

    @property
    def get_testing_df(self):
        testing_by_reg = GetOfficialBGStats()
        testing_df = testing_by_reg.get_by_region_data()
        return testing_df

    def add_exces_official_dt(self, exc_mort_total_loc: str) -> pd.DataFrame:
        exc_mort = exc_mort_total_loc
        df = pd.read_excel(exc_mort, sheet_name='Sheet1')

        new_df = df.merge(self.get_cov_mort_df, on=['Location', 'Sex'])

        new_df['excess/official_mean'] = new_df.apply(lambda x: x['Excess_mortality_Mean'] / x['Covid Mortality'],
                                                      axis=1).round(1)
        new_df['excess/official_fluc'] = new_df.apply(
            lambda x: ((x['Excess_mortality_Mean'] + x['Excess_mortality_fluc']) / x['Covid Mortality']) - x[
                'excess/official_mean'], axis=1).round(1)
        new_df['excess/official ±'] = new_df['excess/official_mean'].map(str) + ' (±' + new_df['excess/official_fluc'].map(
            str) + ')'

        return new_df

    def add_test_pos_data_df(self, exc_mort_total_df: pd.DataFrame) -> pd.DataFrame:
        df = exc_mort_total_df
        df = df[df['Sex'] == 'Total']

        new_df = df.merge(self.get_testing_df, on=['Location'])
        # TODO: fix table column refs
        new_df['CFR'] = new_df.apply(lambda x: (x['Covid Mortality'] / x['Positive Cases'])*100, axis=1).round(1)

        return new_df