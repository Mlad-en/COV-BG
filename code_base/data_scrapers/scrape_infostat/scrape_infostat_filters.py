from typing import Optional, List


def exclude_contiguous_years(start_year_inclusive, end_year_exclusive, except_years: Optional[List] = None) -> List:
    """
    Function generates a list of contiguous years that need to be excluded, if not in the list of except_years.
    :param start_year_inclusive: The starting year to be excluded.
    :param end_year_exclusive: The ending year to be excluded.
    :param except_years: Years to not be excluded if they fall in the interval between the start and end years.
    :return: Returns a list of years to be excluded.
    """
    except_years = except_years if except_years else []
    return [str(year) for year in range(start_year_inclusive, end_year_exclusive) if year not in except_years]


def exclude_multiple_years(start_year_inclusive,
                           end_year_exclusive,
                           interval,
                           except_years: Optional[List] = None) -> List:
    """
    Function generates a list of interval years that need to be excluded, if not in the list of except_years.
    :param start_year_inclusive: The starting year to be excluded.
    :param end_year_exclusive: The ending year to be excluded.
    :param interval: The interval between each year period - i.e. if interval = 2, then the years will be: 2000, 2002,
    2004, etc.
    :param except_years: Years to not be excluded if they fall in the interval between the start and end years.
    :return: Returns a list of years to be excluded.
    """
    except_years = except_years if except_years else []
    return [f'{year} - {year + interval}'
            for year in range(start_year_inclusive, end_year_exclusive)
            if year not in except_years]


class ExcludePopulationByAgeSexRegionFilters:
    """
    Class generates a list of data points to be excluded from the data set.
    """

    exclude_params = {
                'years': exclude_contiguous_years(2001, 2020),
                'additional': ['Urban', 'Rural'],
            }


class ExcludeAverageLifeExpectancyBySexFilters:
    """
    Class generates a list of data points to be excluded from the data set.
    """

    exclude_params = {
        'years': exclude_multiple_years(2006, 2019, 2, [2017]),
        'additional': [],
    }


class ExcludeLifeExpectancyBySexFilters:
    """
    Class generates a list of data points to be excluded from the data set.
    """

    exclude_params = {
        'years': exclude_multiple_years(2008, 2019, 2, [2017]),
        'additional': ['Urban', 'Rural', 'Probability of dying', 'Probability of surviving'],
    }


class ExcludePopulationByMunicipalityFilters:
    """
    Class generates a list of data points to be excluded from the data set.
    """

    exclude_params = {
        'years': exclude_contiguous_years(2000, 2021, except_years=[2019]),
        'additional': ['В градовете', 'В селата'],
    }


class ExcludeMortalityByAgeSexMunicipalityFilters:
    """
    Class generates a list of data points to be excluded from the data set.
    """

    exclude_params = {
        'years': exclude_contiguous_years(2000, 2015),
        'additional': [],
    }
