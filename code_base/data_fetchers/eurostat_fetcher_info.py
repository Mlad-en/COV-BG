from code_base.data_bindings.data_types import EurostatDataSets as DtTp


class EurostatDataFetcherInfo:
    """

    """

    URL = 'https://ec.europa.eu'

    AVAILABLE_DATASETS = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY,
        DtTp.MORTALITY_BY_SEX_AGE_REGION,
        DtTp.POP_BY_SEX_AGE_COUNTRY,
    }

    PAGES = {
        'bulk_data': '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?dir=data',
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY:
            '/eurostat/databrowser/view/demo_r_mwk_05/default/table?lang=en',
        DtTp.MORTALITY_BY_SEX_AGE_REGION:
            '/eurostat/databrowser/view/demo_r_mweek3/default/table?lang=en',
        DtTp.POP_BY_SEX_AGE_COUNTRY:
            '/eurostat/databrowser/view/demo_pjangroup/default/table?lang=en'
    }

    FILES = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY:
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mwk_05.tsv.gz',
        DtTp.MORTALITY_BY_SEX_AGE_REGION:
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mweek3.tsv.gz',
        DtTp.POP_BY_SEX_AGE_COUNTRY:
            '/eurostat/api/dissemination/sdmx/2.1/data/demo_pjangroup/?&format=CSV'
    }

    READ_CSV_PARAMS = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: {
            'encoding': 'utf-8-sig',
            'compression': 'gzip',
            'sep': '\t',
            'low_memory': False
        },
        DtTp.MORTALITY_BY_SEX_AGE_REGION: {
            'encoding': 'utf-8-sig',
            'compression': 'gzip',
            'sep': '\t',
            'low_memory': False
        },
        DtTp.POP_BY_SEX_AGE_COUNTRY: {
            'encoding': 'utf-8-sig',
        },
    }


class EurostatFileInfo:
    """

    """

    def __init__(self, file_type):

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
