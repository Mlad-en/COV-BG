from code_base.data_bindings.data_types import InfostatDataSets as DtTp
from code_base.data_scrapers.scrape_infostat.scrape_infostat_dwnld_strategies import (RequestStrategyInfostatBulgarian,
                                                                                      RequestStrategyInfostatEnglish)
from code_base.data_scrapers.scrape_infostat.scrape_infostat_filters import *


class InfostatFiles:
    """
    Class contains information about the different Infostat files and their scraping parameters.
    """

    URL = 'https://infostat.nsi.bg'

    PAGES = {
        DtTp.POP_BY_SEX_AGE_REG: '/infostat/pages/reports/query.jsf?x_2=1168',
        DtTp.MORTALITY_BY_SEX_AGE_MUN: '/infostat/pages/reports/query.jsf?x_2=1033',
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: '/infostat/pages/reports/query.jsf?x_2=41',
        DtTp.LIFE_EXPECTANCY_BY_SEX: '/infostat/pages/reports/query.jsf?x_2=230',
        DtTp.POP_BY_MUNICIPALITY: '/infostat/pages/reports/query.jsf?x_2=1062'
    }

    LANGUAGES = {
        DtTp.POP_BY_SEX_AGE_REG: 'en',
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: 'en',
        DtTp.LIFE_EXPECTANCY_BY_SEX: 'en',
        DtTp.MORTALITY_BY_SEX_AGE_MUN: 'bg',
        DtTp.POP_BY_MUNICIPALITY: 'bg'
    }

    FILE_FILTER_TYPES = {
        DtTp.POP_BY_SEX_AGE_REG: ExcludePopulationByAgeSexRegionFilters,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: ExcludeAverageLifeExpectancyBySexFilters,
        DtTp.LIFE_EXPECTANCY_BY_SEX: ExcludeLifeExpectancyBySexFilters,
        DtTp.POP_BY_MUNICIPALITY: ExcludePopulationByMunicipalityFilters,
        DtTp.MORTALITY_BY_SEX_AGE_MUN: ExcludeMortalityByAgeSexMunicipalityFilters,
    }

    REQUEST_STRATEGIES = {
        DtTp.POP_BY_SEX_AGE_REG: RequestStrategyInfostatEnglish,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: RequestStrategyInfostatEnglish,
        DtTp.LIFE_EXPECTANCY_BY_SEX: RequestStrategyInfostatEnglish,
        DtTp.MORTALITY_BY_SEX_AGE_MUN: RequestStrategyInfostatBulgarian,
        DtTp.POP_BY_MUNICIPALITY: RequestStrategyInfostatBulgarian
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
