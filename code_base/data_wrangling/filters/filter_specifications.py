from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class Specification:

    def is_satisfied(self, df) -> List:
        pass


class AgeSpecification(Specification):

    def __init__(self, age_range: List):
        self.age_range = age_range

    def is_satisfied(self, df: pd.DataFrame) -> List:
        return list(df[~df[COL_HEAD.AGE].isin(self.age_range)].index)


class SexSpecification(Specification):
    def __init__(self, sex_groups: List):
        self.sex_groups = sex_groups

    def is_satisfied(self, df) -> List:
        return list(df[~df[COL_HEAD.SEX].isin(self.sex_groups)].index)


class LocationSpecification(Specification):
    def __init__(self, locations: List):
        self.locations = locations

    def is_satisfied(self, df) -> List:
        return list(df[df[COL_HEAD.LOCATION].isin(self.locations)].index)


class WeekStartSpecification(Specification):
    def __init__(self, week_start: int):
        self.week_start = week_start

    def is_satisfied(self, df) -> List:
        return list(df[df[COL_HEAD.WEEK].lt(self.week_start)].index)


class WeekEndSpecification(Specification):
    def __init__(self, week_end: int):
        self.week_end = week_end

    def is_satisfied(self, df) -> List:
        return list(df[df[COL_HEAD.WEEK].gte(self.week_end)].index)


class WeekRangeSpecification(Specification):
    def __init__(self, weeks: List):
        self.weeks = weeks

    def is_satisfied(self, df):
        return list(df[~df[COL_HEAD.WEEK].isin(self.weeks)].index)


class AndSpecification(Specification):

    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, df) -> List:
        items = []
        [items.extend(item) for item in map(lambda spec: spec.is_satisfied(df), self.args)]

        return items


class FilterData:

    def __init__(self, spec: Specification):
        self.spec = spec

    def filter_out_data(self, df: pd.DataFrame):
        return df.drop(self.spec.is_satisfied(df), axis=0)
