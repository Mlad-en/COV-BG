from typing import Dict, List

import numpy as np
import pandas as pd
import requests as req


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
    """
    Class only applicable for Bulgaria and Czechia currently. Data for countries is controlled via the
    LIFE_EXPECTANCY_DATA_PACKAGED bindings.
    """
    def __init__(self, country: str):
        self.countries = LIST_LIFE_EXP_DT_COUNTRIES
        if country not in self.countries:
            raise TypeError(f'Incorrect country entered. Only acceptable options are: {", ".join(self.countries)}.')

        self.file_loc = source_le_countries_data
        self.countries: Dict = LIFE_EXPECTANCY_DATA_PACKAGED
        self.country: str = country

    @staticmethod
    def get_data(country_dt: Dict) -> pd.DataFrame:
        url = country_dt['url_dict']['main'] + country_dt['url_dict'][country_dt['page_file']][country_dt['pf_name']]
        request = req.get(url)
        sheet = country_dt.get('sheet_name', 0)
        df = pd.read_excel(request.content, sheet_name=sheet)
        return df

    @staticmethod
    def melt_sex_cols(df: pd.DataFrame, country_dt: Dict) -> pd.DataFrame:
        df = df
        sex = country_dt['rename_columns'][1:]
        df = pd.melt(df, id_vars=['Age'], value_vars=sex, var_name='Sex', value_name='Life_Expectancy')
        return df

    @staticmethod
    def clean_df_cols_rows(df: pd.DataFrame, country_dt: Dict) -> pd.DataFrame:

        df = df

        # Filter on applicable columns in files
        df = df[country_dt['columns']]

        # Limit Data frame to only relevant rows
        index_start_rows = df.index[df[country_dt['start_index'][0]] == country_dt['start_index'][1]].tolist()

        if country_dt.get('end_index'):
            index_end_rows = df.index[df[country_dt['end_index'][0]] == country_dt['end_index'][1]].tolist()
            df = df.iloc[index_start_rows[0] + 1:index_end_rows[0]]
        else:
            df = df.iloc[index_start_rows[0] + 1:]

        df.columns = country_dt['rename_columns']

        df.dropna(how='all', axis=0, inplace=True)

        return df

    def build_data(self, country_dt: Dict) -> str:

        df = self.get_data(country_dt=country_dt)
        df = self.clean_df_cols_rows(df=df, country_dt=country_dt)

        df = self.melt_sex_cols(df=df, country_dt=country_dt)

        df = df.round(2)

        file_loc = self.save_df_to_file(df, self.file_loc, country_dt['lf_ex_clean'])
        return file_loc

    def merge_files(self, files: List[str]) -> str:

        file_men = files[0]
        file_women = files[1]

        df_men = pd.read_csv(file_men, converters={'Age': float})
        df_women = pd.read_csv(file_women, converters={'Age': float})

        dframes = [df_men, df_women]
        both_sexes = pd.concat(dframes)

        file_name = f'{self.country}_life_expectancy_both_sexes'
        file_loc = self.save_df_to_file(both_sexes, self.file_loc, file_name)

        return file_loc

    def get_life_tables(self) -> str:
        country_data = self.countries[self.country]
        if len(country_data) == 1:
            return self.build_data(*self.countries[self.country])

        else:
            files = []
            for file in country_data:
                files.append(self.build_data(file))
            return self.merge_files(files)