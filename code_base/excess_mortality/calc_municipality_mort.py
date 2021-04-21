import os
import warnings

import pandas as pd
from math import sqrt

from code_base.excess_mortality.folder_constants import *
from code_base.excess_mortality.get_infostat_dt import DownloadInfostatDT
from code_base.excess_mortality.get_pop_cntr import get_bg_mun_pop
from code_base.excess_mortality.scraping_constants import BG_MUNICIPALITIES, DECODE_REGION
from code_base.utils.file_utils import SaveFile


class CalcMunMort(SaveFile):
    """
    Todo: Inherit from CalcExcessMortality to take advantage of Excess Mortality and P-score calculation functions.
    """
    def __init__(self):

        self.source_location = source_cov_bg_mun
        self.output_loc = output_excess_mortality_municipalities
        super().__init__()

    @staticmethod
    def read_file(fl) -> pd.DataFrame:
        yearly_mun_mort = fl
        # Catch and suppress UserWarning from openpyxl about "Workbook contains no default style".
        warnings.simplefilter('ignore', category=UserWarning)

        df = pd.read_excel(yearly_mun_mort, sheet_name='Sheet0', engine='openpyxl', skiprows=2, header=[0, 1])
        return df

    def read_cov_file(self) -> pd.DataFrame:
        # File provided by 265 stories about the Economy: https://265obshtini.bg/
        fl = r'mz_covid19_upload.xlsx'
        file_path = os.path.join(self.source_location, fl)
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        return df

    def clean_df(self, fl) -> pd.DataFrame:
        df = self.read_file(fl)
        # Translate municipality names in English
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: BG_MUNICIPALITIES.get(x))

        # Removes Legend At the bottom
        df.dropna(how='any', inplace=True)
        # Convert Male, Female and Total columns to Rows for all years
        new = df.stack([1]).copy()

        # Return to numeric col index and remove resulting incorrect numbering caused by the grouping of the previous col conversion
        new.reset_index(inplace=True)
        new.drop(new.columns[0], axis=1, inplace=True)

        # Backfill values for output_loc to propagate to the sex rows
        new.iloc[:, -1] = new.iloc[:, -1].fillna(method='pad')

        # Rename columns accordingly and reorder columns
        new.rename(columns={new.columns[-1]: 'Location', new.columns[0]: 'Sex'}, inplace=True)
        cols = list(new.columns.values)
        cols = [cols[-1]] + cols[0:-1]
        new = new[cols].copy(deep=True)

        # Remove any columns with empty values - byproduct of the stack function
        new.dropna(how='any', inplace=True)
        sex = {'Жени': 'Female', 'Мъже': 'Male', 'Общо': 'Total'}
        new['Sex'] = new.apply(lambda x: sex.get(x['Sex']), axis=1)

        # add Region information
        new['Region'] = new.apply(lambda x: DECODE_REGION.get(x['Location']), axis=1)
        # Method will not fill in Byala since there are two municipalities in Bulgaria with that name - one in Ruse, and one in Varna.
        # To account for this Region is copied from neighbouring row.
        new['Region'] = new['Region'].fillna(method='backfill')

        # Reorder columns, make region first column
        cols = list(new.columns.values)
        cols = [cols[-1]] + cols[0:-1]
        new = new[cols].copy(deep=True)

        # Convert 2015 data to numeric. For some reason it is read as object, instead of int.
        new['2015'] = new['2015'].map(int)

        # Generate Excess mortality and P-Score calculations, including
        new['STD'] = new.loc[:, ['2015', '2016', '2017', '2018', '2019']].std(axis=1, ddof=0).round(1)
        new['Z-Score(95%)'] = 1.96
        new['Conf_interval'] = new.apply(lambda x: x['Z-Score(95%)'] * (x['STD'] / sqrt(5)), axis=1).round(1)
        new['Mean_Mortality'] = new[['2015', '2016', '2017', '2018', '2019']].mean(axis=1).round(1)
        new['Lower_bound_Mean_mortality'] = new['Mean_Mortality'] - new['Conf_interval'].round(1)
        new['Upper_bound_Mean_mortality'] = new['Mean_Mortality'] + new['Conf_interval'].round(1)

        new['Excess_mortality_Mean'] = new.apply(lambda x: x['2020'] - x['Mean_Mortality'], axis=1).round(1)
        new['Excess_mortality_fluc'] = new.apply(
            lambda x: abs(x['Excess_mortality_Mean'] - (x['2020'] - x['Lower_bound_Mean_mortality'])), axis=1).round(1)

        new['P_Score'] = new.apply(
            lambda x: ((x['2020'] - x['Mean_Mortality']) / x['Mean_Mortality']) * 100 if x['Mean_Mortality'] != 0 else 0,
            axis=1).round(1)

        new['P_score_fluctuation'] = new.apply(
            lambda x: (x['P_Score'] - (
                    ((x['2020'] - x['Upper_bound_Mean_mortality']) / x['Upper_bound_Mean_mortality']) * 100))
            if x['Upper_bound_Mean_mortality'] != 0 else 0,
            axis=1).round(1)

        # Visually represent Mean, Excess Mortality and P-score with their respective confidence intervals
        new['Mean Mortality ±'] = new['Mean_Mortality'].round(1).map(str) + ' (±' + new['Conf_interval'].map(str) + ')'
        new['Excess Mortality ±'] = new['Excess_mortality_Mean'].map(str) + ' (±' + new['Excess_mortality_fluc'].map(
            str) + ')'
        new['P_score ±'] = new['P_Score'].map(str) + '% (±' + new['P_score_fluctuation'].map(str) + '%)'

        return new

    def calc_covid_mort_cfr(self) -> pd.DataFrame:
        """
        :return: Returns a dataframe object containing data about Covid-19 mortality by municipality, including CFR.
        """
        df = self.read_cov_file()

        # Remove legend at the bottom and rename columns appropriately
        df.dropna(how='all', axis=1, inplace=True)
        columns = {df.columns[0]: 'Location',
                   df.columns[1]: 'Diagnosed_Home_Treatment',
                   df.columns[2]: 'Hospitalized',
                   df.columns[3]: 'Total Cases',
                   df.columns[4]: 'Recovered',
                   df.columns[5]: 'Deaths'}
        df.rename(columns=columns, inplace=True)

        # Remove 'Municipality' from the text of the Location column
        df['Location'] = df['Location'].str.replace('Община ', '', regex=False)

        # Translate Municipalities in English
        df['Location'] = df.apply(lambda x: BG_MUNICIPALITIES.get(x['Location']), axis=1)

        # add Region information
        df['Region'] = df.apply(lambda x: DECODE_REGION.get(x['Location']), axis=1)

        # Reorder columns, make region first column
        cols = list(df.columns.values)
        cols = [cols[-1]] + cols[0:-1]
        df = df[cols].copy(deep=True)

        # Calculate Case Fatality Ratio (CFR)
        df['CFR'] = df.apply(lambda x: (x['Deaths'] / x['Total Cases']) * 100, axis=1).round(2)

        # Sort Data by CFR descending
        df.sort_values(by='CFR', ascending=False, inplace=True)

        return df


if __name__ == '__main__':
    # mort_raw = DownloadInfostatDT('mortality_by_age_sex_mun')
    # file = mort_raw.fetch_infostat_data()
    # mort_reg = mort_raw.rename_and_move_file(file, 'infostat_mortality_by_age_sex_mun')
    #
    # pop = DownloadInfostatDT('population_by_municipality')
    # file = pop.fetch_infostat_data()
    # pop_mun = pop.rename_and_move_file(file, 'infostat_population_by_municipality')

    mort = CalcMunMort()
    crfs = mort.calc_covid_mort_cfr()
    mort.save_df_to_file(df=crfs,
                         file_name='BG_covid_19_mortality_by_municipality',
                         location=mort.output_loc,
                         method='excel')

    # dtfrm = mort.clean_df(mort_reg)
    #
    # merge_mort_pop = dtfrm.merge(get_bg_mun_pop(pop_mun), on=['Location', 'Sex', 'Region'])
    # mort.save_df_to_file(df=merge_mort_pop,
    #                      file_name='BG_excess_mortality_by_municipality_and_sex_and_pop',
    #                      location=mort.output_loc,
    #                      method='excel')