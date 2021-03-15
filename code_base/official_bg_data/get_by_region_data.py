from typing import Optional, Dict

import pandas as pd
from requests import post
from bs4 import BeautifulSoup

from code_base.official_bg_data.decode_args import *
from code_base.official_bg_data.url_constants import EGOV_BG
# TODO: Move SaveFile class to separate package
from code_base.excess_mortality.utils import SaveFile


class GetOfficialBGStats(SaveFile):
    data_types = {
        'general',
        'by_region',
        'by_age_groups',
        'by_test_type'
    }

    def __init__(self, data_type):
        self.type = data_type
        self.api_full = EGOV_BG['main'] + EGOV_BG['api']['path']
        self.api_key = EGOV_BG['api']['api_key']
        self.resource = EGOV_BG['api']['resource_uri'][self.type]

    def get_data(self):
        data = {
            "api_key": self.api_key,
            "resource_uri": self.resource
        }

        resp = post(self.api_full, data=data)
        soup = BeautifulSoup(resp.content, 'lxml')
        data = soup.find(lambda tag: tag.name == 'table')
        df = pd.read_html(data.prettify(), header=0)[0]

        df['Дата'] = pd.to_datetime(df['Дата'], format='%Y/%m/%d')

        return df

    def get_by_region_data(self,
                           limit_date: bool = True,
                           year: Optional[int] = 2020,
                           month: Optional[int] = 12,
                           day: Optional[int] = 31) -> pd.DataFrame:
        df = self.get_data()

        df.drop(columns=[col for col in df if
                         col not in BY_REGION_FILT_COLS], inplace=True)

        df.rename(columns=BY_REGION_DECODE_COLUMNS, inplace=True)

        if limit_date:
            filt = F'{year}-{month}-{day}'
            df = df[df['Date'] == filt]

        df = df.melt(id_vars='Date', value_vars=BY_REGION_MELT_VARS,
                     var_name='Location', value_name='Positive Cases')
        df.set_index('Date', inplace=True)
        return df

    # TODO: Implement functions for general stats, by age stats and testing stats.