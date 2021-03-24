from os import path
from typing import List

import pandas as pd

from code_base.excess_mortality.eurostat_bulk_base import (GetBulkEurostatDataBase,
                                                           clean_unneeded_symbols,
                                                           SaveFile,
                                                           UN_LOC_VARS,
                                                           UN_DECODE_AGE_GROUPS,
                                                           UN_DECODE_SEX_GROUPS)
from code_base.excess_mortality.folder_constants import source_eu_population
from code_base.utils.common_query_params import ages_0_84, age_85_89, sex


class GetEUPopulation(GetBulkEurostatDataBase, SaveFile):
    def __init__(self):
        self.eurostat_data = 'europe_population_by_age_and_sex'
        super().__init__(self.eurostat_data, zipped=False)

    def clean_up_df(self) -> None:
        self.split_demographic_data(
            split_from=self.split_columns['split_from_demo'],
            split_into=self.split_columns['split_into_demo'],
            separator=';')

        self.filter_cols(self.retain_demo_columns)

        self.decode_demo_values()

        self.eurostat_df.rename(columns={'2020 ': 'Population'}, inplace=True)
        remove_missing_vals_mask = self.eurostat_df["Population"].str.contains(":") == False
        remove_missing_cntry_mask = self.eurostat_df["Location"].isna()
        self.eurostat_df = self.eurostat_df[remove_missing_vals_mask]
        self.eurostat_df = self.eurostat_df[~remove_missing_cntry_mask]

        self.eurostat_df['Population'] = clean_unneeded_symbols(self.eurostat_df['Population'], 'p', '')
        self.eurostat_df['Population'] = clean_unneeded_symbols(self.eurostat_df['Population'], 'e', '')
        self.eurostat_df['Population'] = self.eurostat_df['Population'].map(int)

    def get_agg_sex_cntry_pop(self, sex: List = ['Total'], age: List = ['Total']) -> pd.DataFrame:
        filt_mask = self.eurostat_df['Sex'].isin(sex) & self.eurostat_df['Age'].isin(age)
        df = self.eurostat_df[filt_mask].copy()
        df.drop('Age', axis=1, inplace=True)
        df = df.groupby(['Sex', 'Location'], as_index=False).sum('Population')
        return df


class GetPopUN(SaveFile):
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

    def get_agg_sex_cntry_pop(self, sex: List = ['Total'], age: List = ['Total']) -> pd.DataFrame:
        filt_mask = (self.pop_df['Sex'].isin(sex)) & (self.pop_df['Age'].isin(age))
        df = self.pop_df[filt_mask].copy()

        df.drop('Age', axis=1, inplace=True)
        df = df.groupby(['Sex', 'Location'], as_index=False).sum('Population')

        return df


if __name__ == '__main__':

    eu = GetEUPopulation()
    eu.clean_up_df()
    eu_lf = eu.get_agg_sex_cntry_pop(age=ages_0_84, sex=sex)

    un = GetPopUN()
    raw_df = un.clean_up_df()
    un_lf = un.get_agg_sex_cntry_pop(age=age_85_89, sex=sex)

    results = pd.concat([eu_lf, un_lf])
    results = results.groupby(['Sex', 'Location'], as_index=False).sum('Population')
