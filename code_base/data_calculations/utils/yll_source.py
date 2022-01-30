from typing import List

import pandas as pd

from code_base.data_bindings.age_group_translations import AGE_BINDINGS
from code_base.data_bindings.data_types import EurostatDataSets
from code_base.data_output import calc_excess_mortality
from code_base.data_wrangling.wrangling_info.local_wrangling_info import LocalStorageWranglingInfo
from code_base.data_wrangling.wrangling_info.who_wrangling_info import WhoWranglingInfo
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_bindings import data_types
from code_base.data_source.get_source_data import get_source_data


class YLLPopulation:

    def __init__(self,
                 years: List[int],
                 ages: List[int],
                 sexes: List[str]):
        self.years = years
        self.ages = ages
        self.sexes = sexes

    @property
    def _has_over_90(self):
        return AGE_BINDINGS.AGE_GE90 in self.ages

    def _get_un_population_over_85(self, include_countries: List[str]):
        un_pop_data = get_source_data(data_types.LocalDataSets.UNDATA_POPULATION)
        wrangler = LocalStorageWranglingInfo(data_types.LocalDataSets.UNDATA_POPULATION).wrangling_strategy

        pop_wrangling = wrangler(self.sexes)

        un_pop_data = pop_wrangling.filter_data(un_pop_data)
        un_pop_data = pop_wrangling.group_data(un_pop_data)

        un_pop_data = un_pop_data.loc[(un_pop_data[COL_HEAD.LOCATION].isin(include_countries)), :]
        return un_pop_data

    def _get_italy_population_over_85(self):
        italy_pop_data = get_source_data(data_types.LocalDataSets.ITALY_POPULATION)
        wrangler = LocalStorageWranglingInfo(data_types.LocalDataSets.ITALY_POPULATION).wrangling_strategy

        pop_wrangling = wrangler([AGE_BINDINGS.AGE_85_89, AGE_BINDINGS.AGE_GE90],
                                 self.sexes)

        italy_pop_data = pop_wrangling.group_data(italy_pop_data)
        italy_pop_data = pop_wrangling.filter_data(italy_pop_data)
        italy_pop_data[COL_HEAD.LOCATION] = 'Italy'
        return italy_pop_data

    def _get_population_eu_lt_85(self):
        pop_type = data_types.EurostatDataSets.POP_BY_SEX_AGE_COUNTRY
        eu_pop_data = get_source_data(pop_type, analyze_years=self.years)
        eu_pop = calc_excess_mortality.CalcEUCountryPop(data_type=pop_type)
        calc_pop = eu_pop.calculate(eu_pop_data, self.ages, self.sexes, group_by='asl')
        return calc_pop

    def get_full_population(self):
        pop_eu = self._get_population_eu_lt_85()

        countries_of_interest = pop_eu[COL_HEAD.LOCATION].unique()
        un_pop_over_85 = self._get_un_population_over_85(countries_of_interest)
        italy_pop_over_85 = self._get_italy_population_over_85()
        pop_eu = pd.concat([pop_eu, un_pop_over_85, italy_pop_over_85], join='inner', axis=0)

        if not self._has_over_90:
            pop_eu = pop_eu.loc[~(pop_eu[COL_HEAD.AGE] == AGE_BINDINGS.AGE_GE90), :]

        return pop_eu


class YLLExcessMortality:

    def __init__(self,
                 years: List[int],
                 ages: List[int],
                 sexes: List[str],
                 from_week: int):
        self.years = years
        self.ages = ages
        self.sexes = sexes
        self.from_week = from_week

    def get_excess_mortality(self) -> pd.DataFrame:
        mort_type = EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
        eu_mort_data = get_source_data(mort_type, analyze_years=self.years)

        excess_mort = calc_excess_mortality.CalcExcessMortalityPredicted(data_type=mort_type, all_years=self.years)
        calc_mort = excess_mort.calculate(eu_mort_data,
                                          self.ages,
                                          self.sexes,
                                          self.from_week,
                                          group_by='all',
                                          predict_on='sla')

        retain_cols = [COL_HEAD.AGE,
                       COL_HEAD.SEX,
                       COL_HEAD.LOCATION,
                       COL_HEAD.EXCESS_MORTALITY_BASE,
                       COL_HEAD.CONFIDENCE_INTERVAL,
                       COL_HEAD.IS_SIGNIFICANT]

        calc_mort.drop(columns=[col for col in calc_mort if col not in retain_cols], inplace=True)

        return calc_mort


class YLLLifeExpectancy:

    def __init__(self, ages: List[int], static_over_90: bool):

        self.ages = ages
        self.static_over_90 = static_over_90

    @property
    def _has_over_85(self):
        return AGE_BINDINGS.AGE_85_89 in self.ages

    def get_life_expectancy(self):
        life_expectancy = get_source_data(data_types.WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX)
        wrangler = WhoWranglingInfo(data_types.WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX).wrangling_strategy

        le_wrangling = wrangler(self._has_over_85, self.static_over_90)

        life_expectancy = le_wrangling.wrangle_data(life_expectancy)

        return life_expectancy


class YLLWorkingYears:

    @staticmethod
    def gen_working_years() -> pd.DataFrame:
        working_years = {
            'Age': ['(15-19)', '(20-24)', '(25-29)', '(30-34)', '(35-39)', '(40-44)', '(45-49)', '(50-54)', '(55-59)',
                    '(60-64)'],
            'Mean_Age_Per_Group': [17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5, 62.5],
            'Working_Years_Left_Mean': [47, 42.5, 37.5, 32.5, 27.5, 22.5, 17.5, 12.5, 7.5, 2.5]
        }
        return pd.DataFrame(working_years)


class GetStandardPopulation:

    def __init__(self, sex: List[str]):
        self.sex = sex

    def get_std_population(self) -> pd.DataFrame:
        std_pop = get_source_data(data_types.LocalDataSets.STD_POPULATION_EU)
        wrangler = LocalStorageWranglingInfo(data_types.LocalDataSets.STD_POPULATION_EU).wrangling_strategy

        pop_wrangling = wrangler(self.sex)
        std_pop = pop_wrangling.filter_data(std_pop)
        std_pop = pop_wrangling.group_data(std_pop)

        return std_pop
