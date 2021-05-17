import os

import pandas as pd

from code_base.excess_mortality.folder_constants import source_cov_bg_comb, output_excess_mortality_regions
from code_base.official_bg_data.get_official_bg_data import GetOfficialBGStats
from code_base.utils.file_utils import SaveFileMixin


class CovMortAttrs(SaveFileMixin):
    """
    Class only used for the Total (all age groups) age-aggregated data for Bulgarian regions.
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

    @staticmethod
    def get_testing_df(year: int = 2020, month: int = 12, day: int = 31):
        testing_by_reg = GetOfficialBGStats()
        testing_df = testing_by_reg.get_by_region_data(year=year, month=month, day=day)
        return testing_df

    def add_exces_official_dt(self, exc_mort_df: pd.DataFrame) -> pd.DataFrame:
        """
        :param exc_mort_total_loc: The path to the excess mortality dataset for Bulgaria by region.
        :return: Returns a dataframe object with the excess mortality data, including Covid-19 related deaths
        and a Excess to Official Covid-19 deaths ratio.
        """
        new_df = exc_mort_df.merge(self.get_cov_mort_df, on=['Location', 'Sex'])

        new_df['excess/official_mean'] = new_df.apply(lambda x:
                                                      x['Excess_mortality_Mean'] / x['Covid Mortality'],
                                                      axis=1).round(1)

        new_df['excess/official_fluc'] = new_df.apply(lambda x:
                                                      (
                                                              (x['Excess_mortality_Mean'] + x['Excess_mortality_fluc'])
                                                       / x['Covid Mortality']
                                                      )
                                                      - x['excess/official_mean'],
                                                      axis=1).round(1)

        new_df['excess/official ±'] = new_df['excess/official_mean'].map(str) + ' (±' + new_df['excess/official_fluc'].map(
            str) + ')'

        return new_df

    def add_test_pos_data_df(self,
                             exc_mort_total_df: pd.DataFrame,
                             year: int = 2020,
                             month: int = 12,
                             day: int = 31) -> pd.DataFrame:
        """The function takes in the Total excess mortality (aggregated ALL ages) for Bulgaria and adds all positive test
        cases for the given period (by default the 31st of December 2020).
        :param exc_mort_total_df:
        :param year: The year to cap off testing information at. Should not be smaller than 2020.
        :param month: The month to cap off testing information at.
        :param day: The day to cap off testing information at.
        :return: Returns a dataframe object that contains the excess mortality for Bulgaria,
         as well as the Positive test cases for a given period. It also calculates the Case Fatality ratio between
         Covid-19 fatalities and positive tests.
        """
        df = exc_mort_total_df

        # Since testing data is NOT sex-stratified, data can only be extracted for the Total cases, regardless of sex.
        df = df[df['Sex'] == 'Total']

        new_df = df.merge(self.get_testing_df(year=year, month=month, day=day), on=['Location'])

        new_df['CFR'] = new_df.apply(lambda x: (x['Covid Mortality'] / x['Positive Cases'])*100, axis=1).round(1)

        return new_df