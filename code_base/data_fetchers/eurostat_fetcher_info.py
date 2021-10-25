class EurostatDataFetcherInfo:
    """

    """

    URL = 'https://ec.europa.eu'

    AVAILABLE_DATASETS = {
        'excess_mortality_by_sex_age_country',
        'excess_mortality_by_sex_age_nuts3',
        'europe_population_by_age_and_sex'
    }

    PAGES = {
        'bulk_data': '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?dir=data',
        'excess_mortality_by_sex_age_country':
            '/eurostat/databrowser/view/demo_r_mwk_05/default/table?lang=en',
        'excess_mortality_by_sex_age_nuts3':
            '/eurostat/databrowser/view/demo_r_mweek3/default/table?lang=en',
        'europe_population_by_age_and_sex':
            '/eurostat/databrowser/view/demo_pjangroup/default/table?lang=en'
    }

    FILES = {
        'excess_mortality_by_sex_age_country':
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mwk_05.tsv.gz',
        'excess_mortality_by_sex_age_nuts3':
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mweek3.tsv.gz',
        'europe_population_by_age_and_sex':
            '/eurostat/api/dissemination/sdmx/2.1/data/demo_pjangroup/?&format=CSV'
    }

    READ_CSV_PARAMS = {
        'excess_mortality_by_sex_age_country': {
            'encoding': 'utf-8-sig',
            'compression': 'gzip',
            'sep': '\t',
            'low_memory': False
        },
        'excess_mortality_by_sex_age_nuts3': {
            'encoding': 'utf-8-sig',
            'compression': 'gzip',
            'sep': '\t',
            'low_memory': False
        },
        'europe_population_by_age_and_sex': {
            'encoding': 'utf-8-sig',
        },
    }


class EurostatFileInfo:
    """

    """

    def __init__(self, file_type):
        if file_type not in EurostatDataFetcherInfo.AVAILABLE_DATASETS:
            available_datasets = ', '.join(EurostatDataFetcherInfo.AVAILABLE_DATASETS)
            raise ValueError(f'Incorrect file type selected. Available file types: {available_datasets}')

        self._file_type = file_type

    @property
    def file_url(self):
        """
        :return:
        """
        url = EurostatDataFetcherInfo.URL
        page = EurostatDataFetcherInfo.FILES[self._file_type]
        return url + page

    @property
    def page_url(self):
        """
        :return:
        """
        url = EurostatDataFetcherInfo.URL
        page = EurostatDataFetcherInfo.PAGES[self._file_type]
        return url + page

    @property
    def csv_params(self):
        """
        :return:
        """
        return EurostatDataFetcherInfo.READ_CSV_PARAMS[self._file_type]
