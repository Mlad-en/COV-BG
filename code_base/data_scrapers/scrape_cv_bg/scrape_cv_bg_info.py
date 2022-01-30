from code_base.data_bindings.data_types import CoronaVirusBGDataSets as DtTp


class CoronaVirusBGConfig:

    URL = 'https://data.egov.bg'

    PATH = '/resource/download/'

    FULL_URL = URL + PATH

    RESOURCES = {
        DtTp.GENERAL:                 'e59f95dd-afde-43af-83c8-ea2916badd19',
        DtTp.BY_REGION:               'cb5d7df0-3066-4d7a-b4a1-ac26525e0f0c',
        DtTp.BY_AGE_GROUP:            '8f62cfcf-a979-46d4-8317-4e1ab9cbd6a8',
        DtTp.BY_TEST_TYPE:            '0ce4e9c3-5dfc-46e2-b4ab-42d840caab92',
        DtTp.DECEASED_BY_SEX_AGE:     '18851aca-4c9d-410d-8211-0b725a70bcfd',
        DtTp.VACCINATED_INFECTED:     'e9f795a8-0146-4cf0-9bd1-c0ba3d9aa124',
        DtTp.VACCINATED_HOSPITALIZED: '6fb4bfb1-f586-45af-8dd2-3385499c3664',
        DtTp.VACCINATED_ICU:          '218d49de-88a8-472a-9bb2-b2a373bd7ab4',
        DtTp.VACCINATED_DECEASED:     'e6a72183-28e0-486a-b4e4-b5db8b60a900',
    }

class CoronaVirusBGFileInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def file_url(self):
        basic_url = CoronaVirusBGConfig.FULL_URL
        resource = CoronaVirusBGConfig.RESOURCES[self._data_type]
        file_extension = '/csv'
        return basic_url + resource + file_extension
