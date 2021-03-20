from typing import List

import pandas as pd

from code_base.excess_mortality.eurostat_bulk_base import GetBulkEurostatDataBase, clean_unneeded_symbols, SaveFile
from code_base.excess_mortality.folder_constants import source_eu_population


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

    def get_age_sex_cntry_pop(self, sex: List = ['Total'], age: List = ['Total']) -> pd.DataFrame:
        filt_mask = self.eurostat_df['Sex'].isin(sex) & self.eurostat_df['Age'].isin(age)
        df = self.eurostat_df[filt_mask].copy()
        df.groupby(['Sex', 'Age', 'Location'], as_index=False).sum('Population')
        return df

