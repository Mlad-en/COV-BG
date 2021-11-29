from typing import List, Optional

from code_base.data_calculations.calc_excess_mortality import CalculateEurostatExcessMortality
from code_base.data_source.get_source_data import get_source_data
from code_base.data_wrangling.wrangling_info.eurostat_wrangling_info import EurostatWranglingInfo


class CalcExcessMortality:

    def __init__(self, data_type):
        self.wrangling_info = EurostatWranglingInfo(data_type)
        self.mortality_calculations = CalculateEurostatExcessMortality()

    @property
    def _exclude_regions(self):
        return self.wrangling_info.default_exclude_regions

    def _group_data(self, group_by):
        return self.wrangling_info.group_by_data(group_by)

    def _wrangling_strategy(self, age_groups: List, sex_groups: List,
                            start_week: int, end_week: int, years: List, group_by):

        grouping = self._group_data(group_by)
        return self.wrangling_info.wrangling_strategy(age=age_groups,
                                                      sex=sex_groups,
                                                      location=self._exclude_regions,
                                                      group_by=grouping,
                                                      start_week=start_week,
                                                      end_week=end_week,
                                                      years=years)

    def calc_mortality(self,
                       clean_data,
                       age_groups: List,
                       sex_groups: List,
                       start_week: int,
                       all_years: List,
                       analyze_year: int,
                       compare_years: List,
                       end_week: Optional[int] = None,
                       group_by: str = 'sl'):

        """

        :param clean_data:
        :param age_groups:
        :param sex_groups:
        :param start_week:
        :param all_years:
        :param analyze_year:
        :param compare_years:
        :param end_week:
        :param group_by:
        :return:
        """

        wrangling_strategy = self._wrangling_strategy(age_groups, sex_groups, start_week, end_week, all_years, group_by)

        data = wrangling_strategy.filter_data(clean_data)
        data = self.mortality_calculations.add_mean_mort(data, compare_years)
        data = wrangling_strategy.group_data(data)
        data = self.mortality_calculations.calculate_excess_mortality(data, compare_years, analyze_year)

        return data
