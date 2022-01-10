from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as HEADERS
from code_base.data_bindings.sex_translations import SEX_BINDINGS as SEXES, InfostatBGSexBindings


class InfostatHeaders:
    FEMALE_BG = InfostatBGSexBindings.FEMALE
    FEMALE_EN = SEXES.FEMALE

    MALE_BG = InfostatBGSexBindings.MALE
    MALE_EN = SEXES.MALE

    AGE = HEADERS.AGE
    SEX = HEADERS.SEX
    YEAR = HEADERS.YEAR
    YEAR_SEX = HEADERS.YEAR + '_' + HEADERS.SEX

    LOCATION = HEADERS.LOCATION
    POPULATION = HEADERS.POPULATION
    LIFE_EXPECTANCY = HEADERS.LIFE_EXPECTANCY
    MORTALITY = HEADERS.MORTALITY

    TOTAL = SEXES.TOTAL
    MALE = SEXES.MALE
    FEMALE = SEXES.FEMALE


class InfostatCleaningParams:

    @staticmethod
    def cols_pop_by_age_sex_reg():
        cols = {
            ind + 1: val for ind, val in enumerate([InfostatHeaders.LOCATION,
                                                    InfostatHeaders.AGE,
                                                    InfostatHeaders.TOTAL,
                                                    InfostatHeaders.MALE,
                                                    InfostatHeaders.FEMALE])
        }
        return cols

    @staticmethod
    def cols_avg_life_expectancy_by_sex():
        cols = {
            ind: val for ind, val in enumerate([InfostatHeaders.LOCATION,
                                                InfostatHeaders.TOTAL,
                                                InfostatHeaders.MALE,
                                                InfostatHeaders.FEMALE])
        }
        return cols

    @staticmethod
    def cols_life_expectancy_by_sex():
        cols = {
            ind + 1: val for ind, val in enumerate([InfostatHeaders.AGE,
                                                    InfostatHeaders.TOTAL,
                                                    InfostatHeaders.MALE,
                                                    InfostatHeaders.FEMALE])
        }
        return cols

    @staticmethod
    def cols_mortality_by_age_sex_mun():
        years = range(2015, 2021)
        demography = (InfostatHeaders.TOTAL, InfostatHeaders.MALE, InfostatHeaders.FEMALE)

        col_vals = [f'{year}-{sex}' for year in years for sex in demography]
        cols = {ind + 1: val for ind, val in enumerate(col_vals)}

        cols[0] = InfostatHeaders.LOCATION

        return cols

    @staticmethod
    def cols_population_by_municipality():
        cols = {
            ind: val for ind, val in enumerate([InfostatHeaders.LOCATION,
                                                InfostatHeaders.TOTAL,
                                                InfostatHeaders.MALE,
                                                InfostatHeaders.FEMALE])
        }
        return cols
