from datetime import date
from typing import List, Optional, Union, Tuple

import pandas as pd

from code_base.excess_mortality.cov_mort import GetFullCovidMortality
from code_base.pyll.decode_vars import LIST_LIFE_EXP_DT_COUNTRIES
from code_base.pyll.folder_constants import output_pyll_bg, output_pyll_cz
from code_base.pyll.get_life_data import FullLifeExpectancy
from code_base.utils.save_file_utils import SaveFile


# TODO: FIX Class
class MergeMortalityLifeExpectancy(SaveFile):
    # Class only applicable for Bulgaria and Czechia currently.
    def __init__(self, country):
        self.countries = LIST_LIFE_EXP_DT_COUNTRIES

        if country not in self.countries:
            raise TypeError(f'Incorrect country entered. Only acceptable options are: {", ".join(self.countries)}.')

        self.country = country
        self.directory = {
            'Bulgaria': output_pyll_bg,
            'Czechia': output_pyll_cz
        }

        self.cov_mort_file = GetFullCovidMortality(self.country).get_covid_mortality
        self.life_expectancy_file = FullLifeExpectancy(self.country).get_life_tables()

    def __get_cov_mort_and_lf_expectancy(self,
                                         start_date,
                                         end_date,
                                         start_age,
                                         end_age,
                                         sheet_name) -> str:

        lf_ex = pd.read_csv(self.life_expectancy_file)
        if sheet_name:
            cov_mort = pd.read_excel(self.cov_mort_file, sheet_name=sheet_name)
        else:
            cov_mort = pd.read_csv(self.cov_mort_file)

        cov_mort['Date'] = pd.to_datetime(cov_mort['Date'], format='%Y-%m-%d').dt.date
        cov_mort = cov_mort[
            (cov_mort['Date'] >= date(year=start_date[0], month=start_date[1], day=start_date[2]))
            & (cov_mort['Date'] <= date(year=end_date[0], month=end_date[1], day=end_date[2]))
            & (cov_mort['Age'] >= start_age)
            & (cov_mort['Age'] <= end_age)
            ]

        cov_mort_lf = cov_mort.merge(lf_ex, how='inner', on=['Age', 'Sex']).sort_values(by='Date')

        age = 'all ages' if start_age == 0 and end_age == 150 else f'from {start_age} to {end_age}'
        filename = f'{self.country} - RAW PYLL({age})'
        directory = self.directory[self.country]

        file_path = self.save_df_to_file(df=cov_mort_lf, file_name=filename, location=directory)
        return file_path

    def calc_pyll_cz(self,
                     start_date: Union[List, Tuple] = (2020, 3, 1),
                     end_date: Union[List, Tuple] = (2020, 12, 31),
                     start_age: int = 0,
                     end_age: int = 150,
                     sheet_name: Union[str, int] = 0) -> str:

        file = self.__get_cov_mort_and_lf_expectancy(start_date, end_date, start_age, end_age, sheet_name)
        df = pd.read_csv(file)

        cntr_pyll = df.groupby(['Sex'], as_index=False).agg(TOTAL_PYLL=('Life_Expectancy', 'sum'),
                                                            PERSON_COUNT=('Age', 'count'),
                                                            MEAN_AGE=('Age', 'mean'),
                                                            AVG_PYLL=('Life_Expectancy', 'mean')).round(2)

        age = 'all ages' if start_age == 0 and end_age == 150 else f'from {start_age} to {end_age}'
        filename = f'{self.country} - CALCULATED PYLL({age}).csv'
        directory = self.directory[self.country]

        file_path = self.save_df_to_file(df=cntr_pyll, location=directory, file_name=filename)
        return file_path