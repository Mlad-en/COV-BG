import pandas as pd

from code_base.data_bindings.age_group_translations import AGE_BINDINGS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS


class WHOLifeExpectancyWranglingStrategy:
    """
    Class used to distinguish between 3 modes for Life Expectancy.
    Since WHO data only goes up to age 85+, while Eurostat has age groups up until 90+,
    the current wrangling stategy makes a decision whether to augment  WHO data to include an age group 90+.
    If object created with: add_90_and_over=TRUE && static_over_90=TRUE -> Then age group 90+ is added with a static
    values for all countries.
    If object created with: add_90_and_over=TRUE && static_over_90=FALSE -> Then age group 90+ is added with value for
    age group 85+ for all countries.
    If object created with: add_90_and_over=FALSE -> Then age group 90+ is NOT added.
    """

    def __init__(self,
                 add_90_and_over: bool,
                 static_over_90: bool):
        self.add_90_and_over = add_90_and_over
        self.static_over_90 = static_over_90

    @staticmethod
    def generate_over_90(data):
        """

        :param data:
        :return:
        """
        age = COLUMN_HEADING_CONSTS.AGE
        age_group_from = AGE_BINDINGS.AGE_85_89
        age_group_to = AGE_BINDINGS.AGE_GE90

        temp_df = data[data[age] == age_group_from]
        temp_df[age].values[:] = temp_df[age].str.replace(age_group_from,
                                                          age_group_to,
                                                          regex=False)

        return temp_df

    def generate_static_over_90(self, data):
        """
        :param temp_df:
        :return:
        """
        temp_df = self.generate_over_90(data)
        temp_df[COLUMN_HEADING_CONSTS.LIFE_EXPECTANCY].values[:] = 4
        return temp_df

    def wrangle_data(self, data):
        """
        If object created with: add_90_and_over=TRUE && static_over_90=TRUE -> Then age group 90+ is added with a static
        values for all countries.
        If object created with: add_90_and_over=TRUE && static_over_90=FALSE -> Then age group 90+ is added with value
        for age group 85+ for all countries.
        If object created with: add_90_and_over=FALSE -> Then age group 90+ is NOT added.
        :param data: Dataframe containing cleaned Life Expectancy Data from WHO.
        :return: Returns Dataframe with or without age group 90+ depending on object settings.
        """

        if self.add_90_and_over and self.static_over_90:
            temp_df = self.generate_static_over_90(data)
            return pd.concat([data, temp_df])

        if self.add_90_and_over:
            temp_df = self.generate_over_90(data)
            return pd.concat([data, temp_df])

        return data
