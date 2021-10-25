from code_base.data_scrapers.scrape_cv_bg.scrape_cv_bg_params import *


class CoronaVirusBGConfig:

    URL = 'https://data.egov.bg'

    PATH = '/resource/download/'

    FULL_URL = URL + PATH

    RESOURCES = {
        'general':                      'e59f95dd-afde-43af-83c8-ea2916badd19',
        'by_region':                    'cb5d7df0-3066-4d7a-b4a1-ac26525e0f0c',
        'by_age_groups':                '8f62cfcf-a979-46d4-8317-4e1ab9cbd6a8',
        'by_test_type':                 '0ce4e9c3-5dfc-46e2-b4ab-42d840caab92',
        'deceased_by_gender_age_group': '18851aca-4c9d-410d-8211-0b725a70bcfd',
        'vaccinated_infections':        'e9f795a8-0146-4cf0-9bd1-c0ba3d9aa124',
        'vaccinated_hospitalized':      '6fb4bfb1-f586-45af-8dd2-3385499c3664',
        'vaccinated_icu':               '218d49de-88a8-472a-9bb2-b2a373bd7ab4',
        'vaccinated_deceased':          'e6a72183-28e0-486a-b4e4-b5db8b60a900',
    }

    RESOURCE_HEADERS = {
        'general':                      CV_BG_GENERAL_DISTRIBUTION_STATISTICS,
        'by_region':                    CV_BG_DISTRIBUTION_BY_REGION,
        'by_age_groups':                CV_BG_DISTRIBUTION_BY_AGE,
        'by_test_type':                 CV_BG_DISTRIBUTION_BY_TESTS,
        'deceased_by_gender_age_group': CV_BG_DECEASED_BY_GENDER_SEX,
        'vaccinated_infections':        CV_BG_INFECTED_VACCINATED,
        'vaccinated_hospitalized':      CV_BG_HOSPITALIZED_VACCINATED,
        'vaccinated_icu':               CV_BG_ICU_VACCINATED,
        'vaccinated_deceased':          CV_BG_DECEASED_VACCINATED,
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

    @property
    def data_headers(self):
        return CoronaVirusBGConfig.RESOURCE_HEADERS[self._data_type]
