import pytest
import requests as req

from code_base.data_bindings.data_types import InfostatDataSets
from code_base.data_scrapers.scrape_infostat.scrape_infostat_file_info import InfostatFileInfo


@pytest.mark.url_check
@pytest.mark.parametrize('file_type',
                         [InfostatDataSets.POP_BY_SEX_AGE_REG,
                          InfostatDataSets.AVG_LIFE_EXPECTANCY_BY_SEX,
                          InfostatDataSets.LIFE_EXPECTANCY_BY_SEX,
                          InfostatDataSets.MORTALITY_BY_SEX_AGE_MUN,
                          InfostatDataSets.POP_BY_MUNICIPALITY])
def test_url_response(file_type):
    url = InfostatFileInfo(file_type=file_type).file_url
    resp = req.get(url)
    assert resp.status_code == 200
