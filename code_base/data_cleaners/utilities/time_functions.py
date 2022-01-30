from datetime import date, datetime
from typing import List


def weeks_in_year(year: int) -> int:
    """
    Per ISO 8601,the last week of the year always contains the 28th of Dec.
    https://en.wikipedia.org/wiki/ISO_week_date#Last_week

    :param year: Year for which last week number is required
    :return: Returns the last week number for a given year (53 weeks or 52 weeks).
    """
    last_week = date(year, 12, 28)
    return last_week.isocalendar()[1]


def generate_week_years(analyze_years) -> List:
    """
    The method generates a list of all years between 2015 and the current year. It then generates the week numbers for
    each year (52/53 depending for past years, depending on the year). For the current year it generates week numbers
    until the current week number of the year.

    :return: Returns a list of Year/Week for each year between 2015 and current year, in the following format:
    'YEAR<W>WEEK_NUMBER'
    e.g. '2020W53 '
    These strings correspond to column headers in Eurostat Mortality files.
    """
    week_years = []

    for year in analyze_years:
        end_range_incl = weeks_in_year(year) if year < datetime.today().year else datetime.today().isocalendar()[1]

        for week in range(1, end_range_incl + 1):
            week_years.append(f'{year}W{str(week).zfill(2)}')

    return week_years