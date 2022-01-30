import time
from abc import ABC, abstractmethod

from code_base.data_scrapers.scrape_infostat.scrape_infostat_page_objects import *
from code_base.data_scrapers.utils import PageObjectActions


class BaseRequestStrategyInfostat(ABC):
    """
    Page strategy base for downloading files from InfoStat.
    """

    def __init__(self, page_actions: PageObjectActions, file_language, file_filters, url):
        self.page_actions = page_actions
        self.file_language = file_language
        self.file_filters = file_filters
        self.url = url
        super().__init__()

    def go_to_results_page(self):
        """
        Function used to go to the results page of Infostat.
        :return: Function returns None.
        """
        request_btn_type = DECODE_BUTTONS['request'][self.file_language]
        self.page_actions.click_all_similar_elements(REQUEST_BUTTON['locator_type'],
                                                     REQUEST_BUTTON['obj'].replace('REPLACE_TEXT', request_btn_type),
                                                     raise_error=False)

        self.page_actions.wait_url_change(self.url)

    def filter_first_page(self):
        """
        Function used to select data on the filters page of Infostat for a given data type.
        :return: Function returns None.
        """
        self.page_actions.click_all_similar_elements(CHECK_ALL_PARENT_CHECKBOXES['locator_type'],
                                                     CHECK_ALL_PARENT_CHECKBOXES['objs'])
        time.sleep(2)
        self.page_actions.click_all_specific_elements(UNCHECK_SPECIFIC_CHECKBOXES['locator_type'],
                                                      [UNCHECK_SPECIFIC_CHECKBOXES['objs'].replace('REPLACE_TEXT', el)
                                                       for el in self.file_filters])

    @abstractmethod
    def request_data(self):
        """
        Function scrapes data from Infostat.
        :return: None
        """
        pass


class RequestStrategyInfostatBulgarian(BaseRequestStrategyInfostat):
    """
    Class used to scrape data sets in Bulgarian.
    """

    def __init__(self, page_actions: PageObjectActions, file_language, file_filters, url):
        super().__init__(page_actions, file_language, file_filters, url)

    def request_data(self):
        super().filter_first_page()

        time.sleep(2)

        self.page_actions.click_all_similar_elements(UNCHECK_NUTS2_REGIONS['locator_type'],
                                                     UNCHECK_NUTS2_REGIONS['objs'])

        time.sleep(2)

        super().go_to_results_page()
        self.page_actions.wait_for_elements(WAIT_FOR_DEMO_ELEMENTS_BG, 20)


class RequestStrategyInfostatEnglish(BaseRequestStrategyInfostat):
    """
    Class used to scrape data sets in English.
    """

    def __init__(self, page_actions: PageObjectActions, file_language, file_filters, url):
        super().__init__(page_actions, file_language, file_filters, url)

    def request_data(self):
        self.page_actions.find_and_click_element(SWITCH_TO_ENGLISH['locator_type'], SWITCH_TO_ENGLISH['obj'])

        time.sleep(5)

        super().filter_first_page()
        super().go_to_results_page()
        self.page_actions.wait_for_elements(WAIT_FOR_DEMO_ELEMENTS_EN, 20)
