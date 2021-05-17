from os import path

import pandas as pd


from code_base.excess_mortality.folder_constants import source_cov_mort_cz, source_cov_bg_comb
from code_base.excess_mortality.url_constants import CZ_COV_URL
from code_base.pyll.decode_vars import LIST_LIFE_EXP_DT_COUNTRIES
from code_base.utils.file_utils import SaveFileMixin


class GetFullCovidMortality(SaveFileMixin):

    def __init__(self, country):
        self.countries = LIST_LIFE_EXP_DT_COUNTRIES

        if country not in self.countries:
            raise TypeError(f'Incorrect country entered. Only acceptable options are: {", ".join(self.countries)}.')

        self.locs = {'Bulgaria': source_cov_bg_comb, 'Czechia': source_cov_mort_cz}
        self.country = country
        self.location = self.locs[self.country]

    def __bg_mortality(self):
        # Mortality for Bulgaria was partially scrapped and partially collected manually due to inconsistent entries
        # at the beginning of the pandemic. For these reasons, calling the scraping function directly
        # is time-intensive and laborious. It would also be incomplete, since it cannot read data earlier on consistently.
        # Hence the processed file is called directly, instead of calling for fresh data.
        bg_mortality = path.join(self.location, 'Combined_bg_Cov_19_mortality.xlsx')
        return bg_mortality

    def __get_cz_cov_mortality(self) -> str:
        url = CZ_COV_URL['main'] + CZ_COV_URL['files']['mortality_by_age_gender']
        df = pd.read_csv(url)

        df['datum'] = pd.to_datetime(df['datum'], format='%Y-%m-%d').dt.date
        df['Sex'] = df.apply(lambda x: 'Male' if x['pohlavi'] == 'M' else 'Female', axis=1)

        df.rename(columns={'datum': 'Date', 'vek': 'Age'}, inplace=True)
        df = df[['Date', 'Age', 'Sex']]

        file_name = 'cz_covid_19_mortality_by_age_gender'
        file_path = self.save_df_to_file(df=df, location=self.location, file_name=file_name)
        return file_path

    @property
    def get_covid_mortality(self):
        func = {'Bulgaria': self.__bg_mortality, 'Czechia': self.__get_cz_cov_mortality}
        return func[self.country]()