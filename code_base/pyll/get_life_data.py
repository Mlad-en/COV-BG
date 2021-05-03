from typing import Dict, List

import numpy as np
import pandas as pd
import requests as req

from code_base.excess_mortality.get_infostat_dt import DownloadInfostatDT
from code_base.pyll.folder_constants import source_WHO_life_data, source_le_countries_data
from code_base.utils.file_utils import SaveFile
from code_base.pyll.decode_loc_vars import EU_COUNTRIES_ISO_3_DECODES
from code_base.pyll.decode_vars import *
from code_base.pyll.url_constants import WHO_DATA


class GetWHOLifeData(SaveFile):
    def __init__(self):
        self.file_loc = source_WHO_life_data

    @staticmethod
    def get_life_tables_eu(location: str = 'EUR',
                           year: str = '2019',
                           add_90_and_over: bool = False,
                           static_over_90: bool = False) -> pd.DataFrame:

        life_tables = WHO_DATA['api']['life_tables_europe']
        life_tables = life_tables.replace('###REGION###', location).replace('###YEAR###', year)
        url = WHO_DATA['main'] + life_tables

        df = pd.read_csv(url, encoding='utf-8-sig')

        drop_columns = ['GHO', 'PUBLISHSTATE', 'REGION',
                        'WORLDBANKINCOMEGROUP', 'Display Value',
                        'Low', 'High', 'Comments']
        df.drop(drop_columns, axis=1, inplace=True)

        rename_columns = {'YEAR': 'Year',
                          'COUNTRY': 'Location',
                          'AGEGROUP': 'Age',
                          'SEX': 'Sex',
                          'Numeric': 'Life_Expectancy'}
        df.rename(columns=rename_columns, inplace=True)

        df['Age'] = df.apply(lambda x: DECODE_WHO_AGE_RANGES.get(x['Age'], np.nan), axis=1)
        df['Sex'] = df.apply(lambda x: DECODE_WHO_GENDER_VARS.get(x['Sex'], np.nan), axis=1)
        df['Location'] = df.apply(lambda x: EU_COUNTRIES_ISO_3_DECODES.get(x['Location'], np.nan), axis=1)
        df.dropna(how='any', axis=0, inplace=True)

        if add_90_and_over:
            temp_df = df[df['Age'] == '(85-89)']
            temp_df['Age'].values[:] = temp_df['Age'].str.replace('(85-89)', '(90+)', regex=False)
            if static_over_90:
                temp_df['Life_Expectancy'].values[:] = 4
            df = pd.concat([df, temp_df])

        return df


class FullLifeExpectancy(SaveFile):

    def __init__(self, country):
        if country not in ('Bulgaria', 'Czechia'):
            raise ValueError('Invalid Country selected.')
        self.country = country
        self.file_loc = source_le_countries_data
        super().__init__()

    @staticmethod
    def cz_life_tbls() -> pd.DataFrame:
        """
        :return: Returns combined life table data for both sexes for Czechia.
        """
        df = pd.DataFrame()
        # Life tables for Czechia exist as two separate files on the Czech's Statistical Office' website.
        # The loop below cleans and combines the two files.
        for values in DECODE_CZ_DT.values():
            url = values['url_dict']['main']
            location = values['url_dict'][values['pages_files']][values['pf_name']]
            full_url_path = url + location
            df_temp = pd.read_excel(full_url_path, skiprows=2, engine='openpyxl')

            # Keep only Age and Life Expectancy columns
            df_temp = df_temp[values['keep_cols']]
            # Translate columns
            columns = values['rename_cols']
            df_temp.rename(columns=columns, inplace=True)
            # Add sex since missing in files.
            df_temp['Sex'] = values['Sex']
            # Add to empty Dataframe.
            df = pd.concat([df, df_temp])

        return df

    @staticmethod
    def bg_life_tbls() -> pd.DataFrame:
        """
        Function scrapes Infostat - A website by the National Statistics' Office of Bulgaria.
        The Function then cleans the returned file and returns a DataFrame.
        :return: DataFrame of Life Expectancy for Bulgaria.
        """
        # Scrape data From InfoStat
        c = DownloadInfostatDT('life_expectancy_by_sex')
        file = c.fetch_infostat_data()
        # Move file from Infostat Download Bin to Source File dir.
        lf_exp = c.rename_and_move_file(file, 'infostat_life_expectancy_by_sex')
        df = pd.read_excel(lf_exp, sheet_name='Sheet0', engine='openpyxl', skiprows=3, header=0)
        # Remove bottom empty values
        df.dropna(how='any', axis=0, inplace=True)
        # Remove first column as it pertains to distinction between Total, Urban and Non-urban areas -
        # hence irrelevant to the current level of analysis.
        df.drop(df.columns[0], axis=1, inplace=True)
        df.rename(columns={df.columns[0]: 'Age'}, inplace=True)
        # Replace 100+ with just the number 100.
        df['Age'] = df['Age'].str.replace('+', '', regex=False)
        # Convert Total, Male and Female columns into a single one - sex.
        df = df.melt(id_vars='Age', value_vars=['Total', 'Male', 'Female'], var_name='Sex', value_name='Life_Expectancy')
        return df

    def get_life_tables(self):
        country_method = {
            'Bulgaria': self.bg_life_tbls,
            'Czechia': self.cz_life_tbls
        }

        df = country_method[self.country]()
        file_name = self.country + '_life_expectancy'
        file_path = self.save_df_to_file(df, source_le_countries_data, file_name=file_name)

        return file_path