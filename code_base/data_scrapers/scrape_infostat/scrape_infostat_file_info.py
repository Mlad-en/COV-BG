from code_base.data_scrapers.scrape_infostat.scrape_infostat_dwnld_strategies import (RequestStrategyInfostatBulgarian,
                                                                                      RequestStrategyInfostatEnglish)
from code_base.data_scrapers.scrape_infostat.scrape_infostat_filters import *


class InfostatFiles:
    """
    Class contains information about the different Infostat files and their scraping parameters.
    """

    URL = 'https://infostat.nsi.bg'

    PAGES = {
        'bg_pop_by_age_sex_reg': '/infostat/pages/reports/query.jsf?x_2=1168',
        'mortality_by_age_sex_mun': '/infostat/pages/reports/query.jsf?x_2=1033',
        'avg_life_expectancy_by_sex': '/infostat/pages/reports/query.jsf?x_2=41',
        'life_expectancy_by_sex': '/infostat/pages/reports/query.jsf?x_2=230',
        'population_by_municipality': '/infostat/pages/reports/query.jsf?x_2=1062'
    }

    LANGUAGES = {
        'bg_pop_by_age_sex_reg': 'en',
        'avg_life_expectancy_by_sex': 'en',
        'life_expectancy_by_sex': 'en',
        'mortality_by_age_sex_mun': 'bg',
        'population_by_municipality': 'bg'
    }

    FILE_FILTER_TYPES = {
        'bg_pop_by_age_sex_reg': ExcludePopulationByAgeSexRegionFilters,
        'avg_life_expectancy_by_sex': ExcludeAverageLifeExpectancyBySexFilters,
        'life_expectancy_by_sex': ExcludeLifeExpectancyBySexFilters,
        'population_by_municipality': ExcludePopulationByMunicipalityFilters,
        'mortality_by_age_sex_mun': ExcludeMortalityByAgeSexMunicipalityFilters,
    }

    REQUEST_STRATEGIES = {
        'bg_pop_by_age_sex_reg': RequestStrategyInfostatEnglish,
        'avg_life_expectancy_by_sex': RequestStrategyInfostatEnglish,
        'life_expectancy_by_sex': RequestStrategyInfostatEnglish,
        'mortality_by_age_sex_mun': RequestStrategyInfostatBulgarian,
        'population_by_municipality': RequestStrategyInfostatBulgarian
    }


class InfostatFileInfo:
    """
    Class provides scraping information depending on the data type required from infostat.
    """

    def __init__(self, file_type):

        if file_type not in InfostatFiles.PAGES:
            available_pages = ', '.join(InfostatFiles.PAGES.keys())
            raise ValueError(f'Incorrect infostat file type selected. Available file types: {available_pages}')

        self._file_type = file_type

    @property
    def file_url(self):
        """
        :return: Returns the url of the first (filter) page of Infostat for the class instances data type.
        """
        url = InfostatFiles.URL
        page = InfostatFiles.PAGES[self._file_type]
        return url + page

    @property
    def file_language(self):
        """
        :return: Returns the language to be set on the first (filter) page of Infostat.
        """
        return InfostatFiles.LANGUAGES[self._file_type]

    @property
    def file_filters(self):
        """
        :return: Returns the filters to be set on the first (filter) page of Infostat.
        """
        filters = InfostatFiles.FILE_FILTER_TYPES[self._file_type]
        all_filters = filters().exclude_params['years']
        all_filters.extend(filters().exclude_params['additional'])
        return all_filters

    @property
    def request_strategy(self):
        """
        :return: Returns the request scraping strategy for the given instance data type.
        """
        return InfostatFiles.REQUEST_STRATEGIES[self._file_type]
