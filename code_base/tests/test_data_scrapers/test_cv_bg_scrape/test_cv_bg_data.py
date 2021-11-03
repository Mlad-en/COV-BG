import pandas as pd
import pytest
import requests as req

from code_base.data_bindings.data_types import CoronaVirusBGDataSets
from code_base.data_scrapers.scrape_cv_bg.scrape_cv_bg import GetOfficialBGStats
from code_base.data_scrapers.scrape_cv_bg.scrape_cv_bg_info import CoronaVirusBGFileInfo

files = [CoronaVirusBGDataSets.GENERAL,
         CoronaVirusBGDataSets.BY_REGION,
         CoronaVirusBGDataSets.BY_AGE_GROUP,
         CoronaVirusBGDataSets.BY_TEST_TYPE,
         CoronaVirusBGDataSets.DECEASED_BY_SEX_AGE,
         CoronaVirusBGDataSets.VACCINATED_INFECTED,
         CoronaVirusBGDataSets.VACCINATED_HOSPITALIZED,
         CoronaVirusBGDataSets.VACCINATED_ICU,
         CoronaVirusBGDataSets.VACCINATED_DECEASED, ]


@pytest.mark.url_check
@pytest.mark.parametrize('data_type', files)
def test_url_response(data_type):
    url = CoronaVirusBGFileInfo(data_type=data_type).file_url
    resp = req.get(url)
    assert resp.status_code == 200


@pytest.mark.parametrize('data_type', files)
def test_column_headers(data_type):
    info = CoronaVirusBGFileInfo(data_type=data_type)
    url = info.file_url
    expected_headers = [header for header in info.data_headers.keys()]
    actual_headers = list(pd.read_csv(url).columns)
    assert actual_headers == expected_headers


@pytest.mark.parametrize('data_type', files)
def test_data_not_empty(data_type):
    data = GetOfficialBGStats(data_type).get_data()
    assert not data.empty
