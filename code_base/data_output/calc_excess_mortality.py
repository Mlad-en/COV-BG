from typing import List, Optional

from code_base.data_calculations.calc_excess_mortality_meanstats import CalculateEurostatExcessMortalityMean
from code_base.data_calculations.calc_excess_mortality_projected import CalculateExcessMortalityPredicted
from code_base.data_wrangling.wrangling_info.eurostat_wrangling_info import EurostatWranglingInfo
from code_base.data_wrangling.wrangling_info.infostat_wrangling_info import InfostatWranglingInfo


class CalculationsBase:

    @property
    def _exclude_regions(self):
        return self.wrangling_info.default_exclude_regions

    def _group_data(self, group_by):
        return self.wrangling_info.group_by_data(group_by)


class CalcExcessMortalityMean(CalculationsBase):

    def __init__(self, data_type, all_years):
        self.mortality_calculations = CalculateEurostatExcessMortalityMean()
        self.wrangling_info = EurostatWranglingInfo(data_type)
        self.all_years = all_years

    @property
    def _analyze_year(self):
        """

        :return:
        """
        return max(self.all_years)

    @property
    def _compare_to_years(self):
        """

        :return:
        """
        return [year for year in self.all_years if not year == self._analyze_year]

    def _cut_off_point(self, end_week):
        """

        :param end_week:
        :return:
        """
        if end_week:
            return {'end_week': end_week}
        else:
            return {'nat_cut_off_year': self._analyze_year}

    def _wrangling_strategy(self, age_groups: List, sex_groups: List, group_by,
                            start_week: int, years: List, end_week: Optional[int] = None):

        """

        :param age_groups:
        :param sex_groups:
        :param group_by:
        :param start_week:
        :param end_week:
        :param years:
        :return:
        """
        grouping = self._group_data(group_by)
        cut_off = self._cut_off_point(end_week)

        return self.wrangling_info.wrangling_strategy(age=age_groups,
                                                      sex=sex_groups,
                                                      location=self._exclude_regions,
                                                      group_by=grouping,
                                                      start_week=start_week,
                                                      cut_off_point=cut_off,
                                                      years=years)

    def calculate(self, clean_data, age_groups: List, sex_groups: List, start_week: int,
                  end_week: Optional[int] = None, group_by: str = 'sl'):

        """

        :param clean_data:
        :param age_groups:
        :param sex_groups:
        :param start_week:
        :param end_week:
        :param group_by: Options are: 'all', 'asl', 'slw','sl'.
        :return:
        """

        wrangling_strategy = self._wrangling_strategy(age_groups, sex_groups, group_by,
                                                      start_week, self.all_years, end_week)

        data = wrangling_strategy.filter_data(clean_data)
        data = self.mortality_calculations.add_mean_mort(data, self._compare_to_years)
        data = wrangling_strategy.group_data(data)
        data.to_csv('verify_info.csv', index=False, encoding='utf-8-sig')
        data = self.mortality_calculations.calculate_excess_mortality(data, self._compare_to_years, self._analyze_year)

        return data


class CalcEUCountryPop(CalculationsBase):

    def __init__(self, data_type):
        self.wrangling_info = EurostatWranglingInfo(data_type)

    def _wrangling_strategy(self, age_groups: List, sex_groups: List, group_by):
        grouping = self._group_data(group_by)

        return self.wrangling_info.wrangling_strategy(age=age_groups,
                                                      sex=sex_groups,
                                                      location=self._exclude_regions,
                                                      group_by=grouping)

    def calculate(self, clean_data, age_groups: List, sex_groups: List, group_by: str = 'sl'):
        """
        :param clean_data:
        :param age_groups:
        :param sex_groups:
        :param group_by:
        :return:
        """

        wrangling_strategy = self._wrangling_strategy(age_groups, sex_groups, group_by)

        data = wrangling_strategy.filter_data(clean_data)
        data = wrangling_strategy.group_data(data)

        return data


class CalcBGRegionPop(CalculationsBase):

    def __init__(self, data_type):
        self.wrangling_info = InfostatWranglingInfo(data_type)

    def _wrangling_strategy(self, age_groups: List, sex_groups: List, group_by):
        grouping = self._group_data(group_by)

        return self.wrangling_info.wrangling_strategy(age=age_groups,
                                                      sex=sex_groups,
                                                      location=self._exclude_regions,
                                                      group_by=grouping)

    def calculate(self, clean_data, age_groups: List, sex_groups: List, group_by: str = 'sl'):
        """
        :param clean_data:
        :param age_groups:
        :param sex_groups:
        :param group_by:
        :return:
        """

        wrangling_strategy = self._wrangling_strategy(age_groups, sex_groups, group_by)

        data = wrangling_strategy.filter_data(clean_data)
        data = wrangling_strategy.group_data(data)

        return data


class CalcExcessMortalityPredicted(CalculationsBase):

    def __init__(self, data_type, all_years):
        self.mortality_calculations = CalculateExcessMortalityPredicted()
        self.wrangling_info = EurostatWranglingInfo(data_type)
        self.all_years = all_years

    @property
    def _analyze_year(self):
        """

        :return:
        """
        return max(self.all_years)

    @property
    def _compare_to_years(self):
        """

        :return:
        """
        return [year for year in self.all_years if not year == self._analyze_year]

    def _cut_off_point(self, end_week):
        """

        :param end_week:
        :return:
        """
        if end_week:
            return {'end_week': end_week}
        else:
            return {'nat_cut_off_year': self._analyze_year}

    def _wrangling_strategy(self, age_groups: List, sex_groups: List, group_by,
                            start_week: int, years: List, end_week: Optional[int] = None):

        """

        :param age_groups:
        :param sex_groups:
        :param group_by:
        :param start_week:
        :param end_week:
        :param years:
        :return:
        """
        grouping = self._group_data(group_by)
        cut_off = self._cut_off_point(end_week)

        return self.wrangling_info.wrangling_strategy(age=age_groups,
                                                      sex=sex_groups,
                                                      location=self._exclude_regions,
                                                      group_by=grouping,
                                                      start_week=start_week,
                                                      cut_off_point=cut_off,
                                                      years=years)

    def calculate(self, clean_data, age_groups: List, sex_groups: List, start_week: int,
                  end_week: Optional[int] = None, group_by: str = 'slw'):

        """

        :param clean_data:
        :param age_groups:
        :param sex_groups:
        :param start_week:
        :param end_week:
        :param group_by: Options are: 'all', 'slw'. Default is 'slw'.
        :return:
        """

        wrangling_strategy = self._wrangling_strategy(age_groups, sex_groups, group_by,
                                                      start_week, self.all_years, end_week)

        data = wrangling_strategy.filter_data(clean_data)
        data = wrangling_strategy.group_data(data)
        data = self.mortality_calculations.get_predicted_mortality(data, self.all_years, group_by)
        data = self.mortality_calculations.add_excess_mort_calcs(data)

        return data
