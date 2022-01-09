from code_base.data_bindings.data_types import WHODataSets


class WHOIntDataFetcherInfo:
    """

    """

    URL = 'https://apps.who.int'

    AVAILABLE_DATASETS = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX,
    }

    PAGES = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX:
            '/gho/athena/data/GHO/LIFE_0000000035.csv?filter=REGION:EUR;YEAR:###YEAR###',
    }


class WHOIntFileInfo:
    """

    """

    def __init__(self, file_type):

        if file_type not in WHOIntDataFetcherInfo.AVAILABLE_DATASETS:

            data = WHOIntDataFetcherInfo.AVAILABLE_DATASETS
            raise ValueError(f"File Type not included in the available file types set. Available types are: {data}")

        self._file_type = file_type


    @property
    def file_url(self):
        """
        :return:
        """
        url = WHOIntDataFetcherInfo.URL
        page = WHOIntDataFetcherInfo.PAGES[self._file_type]
        return url + page
