from os import path
from typing import List, Optional

import pandas as pd

from code_base.excess_mortality.base_eurostat_bulk import (SaveFileMixin,
                                                           UN_LOC_VARS,
                                                           UN_DECODE_AGE_GROUPS,
                                                           UN_DECODE_SEX_GROUPS)
from code_base.excess_mortality.folder_constants import source_eu_population
from code_base.excess_mortality.get_excess_mortality import BaseBulkEurostatData


class GetEUPopulation(BaseBulkEurostatData):
    def __init__(self):
        self.eurostat_data = 'europe_population_by_age_and_sex'
        super().__init__(self.eurostat_data, zipped=False)

    def clean_up_df(self) -> None:
        self.eurostat_df.columns = [col.rstrip() for col in self.eurostat_df.columns]
        super().clean_up_df()

        # TODO: Add comment explanations to the code.

        self.eurostat_df.rename(columns={'2020': 'Population'}, inplace=True)

        remove_missing_vals_mask = self.eurostat_df['Population'].str.contains(":") == False
        self.eurostat_df = self.eurostat_df[remove_missing_vals_mask]
        self.eurostat_df.dropna(how='any', subset=['Location'], axis=0, inplace=True)

        self.replace_symbols(symbol_to_replace='p', replace_with='', apply_to_cols=['Population'])
        self.replace_symbols(symbol_to_replace='e', replace_with='', apply_to_cols=['Population'])

        self.eurostat_df['Population'] = self.eurostat_df['Population'].map(int)

        return

    def get_agg_sex_cntry_pop(self, sex: Optional[List] = None, age: Optional[List] = None) -> pd.DataFrame:
        sex = ['Total'] if not sex else sex
        age = ['Total'] if not age else age
        filt_mask = self.eurostat_df['Sex'].isin(sex) & self.eurostat_df['Age'].isin(age)
        df = self.eurostat_df[filt_mask].copy()
        df.drop('Age', axis=1, inplace=True)
        df = df.groupby(['Sex', 'Location'], as_index=False).sum('Population')
        return df


class GetPopUN(SaveFileMixin):
    def __init__(self):
        self.file_name = 'UNDATA_Population by age, sex and urban-rural residence_2019.csv'
        self.file_loc = path.join(source_eu_population, self.file_name)
        self.pop_df = pd.read_csv(self.file_loc, encoding='utf-8-sig')

    def clean_up_df(self) -> pd.DataFrame:
        filt_age_cntry_sex_area = (self.pop_df['Country or Area'].isin(UN_LOC_VARS)) \
                                  & (self.pop_df['Age'].isin(UN_DECODE_AGE_GROUPS.keys())) \
                                  & (self.pop_df['Sex'].isin(UN_DECODE_SEX_GROUPS.keys())) \
                                  & (self.pop_df['Area'] == 'Total')
        self.pop_df = self.pop_df[filt_age_cntry_sex_area]

        drop_cols = ['Value Footnotes', 'Record Type', 'Reliability', 'Area', 'Year', 'Source Year']
        self.pop_df.drop(columns=drop_cols, inplace=True)

        cols = {'Country or Area': 'Location', 'Value': 'Population'}
        self.pop_df.rename(columns=cols, inplace=True)

        self.pop_df['Sex'] = self.pop_df.apply(lambda x: UN_DECODE_SEX_GROUPS[x['Sex']], axis=1)
        self.pop_df['Age'] = self.pop_df.apply(lambda x: UN_DECODE_AGE_GROUPS[x['Age']], axis=1)

        return self.pop_df

    def get_agg_sex_cntry_pop(self, sex: List = ['Total'], age: List = ['Total'], drop_age: bool = True) -> pd.DataFrame:
        filt_mask = (self.pop_df['Sex'].isin(sex)) & (self.pop_df['Age'].isin(age))
        df = self.pop_df[filt_mask].copy()
        if drop_age:
            df.drop('Age', axis=1, inplace=True)
            grouping = ['Sex', 'Location']
        else:
            grouping = ['Age', 'Sex', 'Location']
        df = df.groupby(grouping, as_index=False).sum('Population')

        return df