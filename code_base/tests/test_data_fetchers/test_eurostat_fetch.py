import pytest
import requests as req

from code_base.data_bindings.data_types import EurostatDataSets
from code_base.data_fetchers.data_fetchers import FetchEuroStatData
from code_base.data_fetchers.eurostat_fetcher_info import EurostatFileInfo


@pytest.mark.url_check
@pytest.mark.parametrize('file_type',
                         [EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY,
                          EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION,
                          EurostatDataSets.POP_BY_SEX_AGE_COUNTRY])
def test_url_response(file_type):
    url = EurostatFileInfo(file_type=file_type).file_url
    resp = req.get(url)
    assert resp.status_code == 200


@pytest.mark.parametrize('file_type',
                         [EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY,
                          EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION,
                          EurostatDataSets.POP_BY_SEX_AGE_COUNTRY])
def test_data_not_empty(file_type):
    data = FetchEuroStatData(file_type).get_data()
    assert not data.empty
