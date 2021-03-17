from typing import Optional, Dict

import pandas as pd
from requests import post
from bs4 import BeautifulSoup

from code_base.official_bg_data.decode_args import *
from code_base.official_bg_data.url_constants import *
# TODO: Move SaveFile class to separate package
from code_base.excess_mortality.utils import SaveFile


class GetOfficialBGStats(SaveFile):
    data_types = {
        'general',
        'by_region',
        'by_age_groups',
        'by_test_type'
    }

    def __init__(self):
        self.decode_cols = {
            'general': GENERAL_DECODE_COLUMNS,
            'by_region': BY_REGION_DECODE_COLUMNS,
        }

    def get_data(self, data_type) -> pd.DataFrame:
        data_type = data_type
        api_full = EGOV_BG['main'] + EGOV_BG['api']['path']
        api_key = EGOV_BG['api']['api_key']
        resource = EGOV_BG['api']['resource_uri'][data_type]

        data = {
            "api_key": api_key,
            "resource_uri": resource
        }

        resp = post(api_full, data=data)
        soup = BeautifulSoup(resp.content, 'lxml')
        data = soup.find(lambda tag: tag.name == 'table')
        df = pd.read_html(data.prettify(), header=0)[0]

        df.rename(columns=self.decode_cols[data_type], inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

        return df

    def get_by_region_data(self,
                           limit_date: bool = True,
                           year: Optional[int] = 2020,
                           month: Optional[int] = 12,
                           day: Optional[int] = 31) -> pd.DataFrame:
        df = self.get_data('by_region')

        df.drop(columns=[col for col in df if
                         col in BY_REGION_DECODE_COLUMNS], inplace=True)

        if limit_date:
            filt = f'{year}-{month}-{day}'
            df = df[df['Date'] == filt]

        df = df.melt(id_vars='Date', value_vars=BY_REGION_MELT_VARS,
                     var_name='Location', value_name='Positive Cases')
        df.set_index('Date', inplace=True)
        return df

    # TODO: Implement functions for general stats, by age stats and testing stats.
    def get_tests_to_cases_by_week(self,
                                   start_year: int = 2020,
                                   start_month: int = 6,
                                   start_day: int = 8,
                                   end_year: int = 2020,
                                   end_month: int = 12,
                                   end_day: int = 31) -> pd.DataFrame:

        filt_str_dates = f'{start_year}-{str(start_month).zfill(1)}-{str(start_day).zfill(1)}'
        filt_end_dates = f'{end_year}-{str(end_month).zfill(1)}-{str(end_day).zfill(1)}'

        data = self.get_data('general')
        data = data[(data['Date'] >= filt_str_dates) & (data['Date'] <= filt_end_dates)]
        data['Week'] = data['Date'].dt.strftime('%W').map(int) + 1
        data['Year'] = data['Date'].dt.strftime('%Y').map(int)
        df1 = data[['Year', 'Week', 'Tests_Done_24h', 'Confirmed_Cases_24h']]
        df1 = df1.groupby(['Year', 'Week'], as_index=False).sum(['Tests_Done_24h', 'Confirmed_Cases_24h'])
        df1['Percent_Positive_Cases'] = df1.apply(
            lambda x: x['Confirmed_Cases_24h'] / x['Tests_Done_24h'] * 100,
            axis=1).round(1)

        pop_url = EUROSTAT_POPULATION['main'] + EUROSTAT_POPULATION['api']['population']
        population = pd.read_csv(pop_url)['2020 '].values[0]
        df1['Population'] = population
        df1['Population_to_Test'] = df1.apply(lambda x: x['Tests_Done_24h'] / x['Population'] * 100, axis=1).round(1)

        df1.rename(columns=RENAME_WEEKLY_COLUMNS, inplace=True)
        return df1
