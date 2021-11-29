import os
from typing import List, Optional, Dict

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote import webelement

from webdriver_manager.firefox import GeckoDriverManager


def launch_browser(url, headless: bool = True) -> webdriver.WebDriver:
    """
    Function used to start a webdriver session with Chrome.
    :param url: The url that needs to be opened as a starting point by the browser.
    :param headless: Bool value, True by default. If set to false, browser actions are visible.
    :return: Returns a webdriver instance of the chrome.
    """
    # Silence Webdriver Manager console logging.
    os.environ["WDM_LOG_LEVEL"] = '0'

    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")

    browser = webdriver.WebDriver(executable_path=GeckoDriverManager(log_level=0, cache_valid_range=1).install(),
                                  options=options)

    if not headless:
        browser.maximize_window()

    browser.get(url)

    return browser


class FindPageobjects:
    """
    Function contains locator methods for different objects on a given web page.
    """

    def __init__(self, browser: webdriver.WebDriver):
        self.browser = browser

    def wait_element_clickable(self, locator_type: str, pg_obj: str, time=10) -> webelement.WebElement:
        """
        Function attempts to locate a visible element based on the locator type provided.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param pg_obj: The object to be located on a given web page.
        :param time: The time to wait for a given object to display.
        :return: Returns the awaited object if present.
        """
        obj_types = {
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
        }
        obj = WebDriverWait(self.browser, time).until(EC.element_to_be_clickable((obj_types[locator_type], pg_obj)))

        return obj

    def wait_element_visible(self, locator_type: str, pg_obj: str, time=10) -> webelement.WebElement:
        """
        Function attempts to locate a clickable element based on the locator type provided.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param pg_obj: The object to be located on a given web page.
        :param time: The time to wait for a given object to display.
        :return: Returns the awaited object if present.
        """
        obj_types = {
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
        }
        obj = WebDriverWait(self.browser, time).until(EC.visibility_of_element_located((obj_types[locator_type], pg_obj)))
        return obj

    def locate_element(self, locator_type: str, pg_obj: str) -> webelement.WebElement:
        """
        Function used to locate a given element. First it will attempt to locate a clickable element and if it fails,
        it will try to locate a visible element.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param pg_obj: The object to be located on a given web page.
        :return: Returns the awaited object if present.
        """

        try:
            obj = self.wait_element_clickable(locator_type, pg_obj)
            return obj
        except TimeoutException:
            try:
                obj = self.wait_element_visible(locator_type, pg_obj)
                return obj
            except TimeoutException:
                raise ValueError(f'Unable to locate page object: {pg_obj} through {locator_type}.')

    def locate_all_elements(self, locator_type: str, pg_obj: str) -> List:
        """
        Function used to locate all elements of a given type.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param pg_obj: The objects to be located on a given web page.
        :return: Returns the awaited objects or an empty list.
        """
        obj_types = {
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
        }

        objs = self.browser.find_elements(obj_types[locator_type], pg_obj)
        return objs


class PageObjectActions:
    """Class provides actions that can be performed over web elements"""

    def __init__(self, browser):
        self.browser = browser
        self.locators = FindPageobjects(self.browser)
        self.action = ActionChains(self.browser)

    def find_and_click_element(self, locator_type: str, obj: str):
        """
        The function attempts to locate a web element and click on it.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param obj: The object to be located on a given web page.
        :return: The function returns None.
        """
        obj = self.locators.locate_element(locator_type, obj)
        if obj.is_displayed():
            self.action.move_to_element(obj)
            obj.click()
            self.action.perform()

    def find_and_type_into_element(self, locator_type: str, obj: str, text: str):
        """
        The function attempts to locate a web element and type in it.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param obj: The objects to be located on a given web page.
        :param text: The text to typed into the element.
        :return: The function returns None.
        """
        obj = self.locators.locate_element(locator_type, obj)
        self.action.move_to_element(obj)
        obj.send_keys(text)
        self.action.perform()

    def click_all_specific_elements(self, locator_type: str, objs: List):
        """
        The function is used to locate specific list of elements and click on each one.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param objs: The objects to be located on a given web page.
        :return: The function returns None.
        """
        for el in objs:
            self.find_and_click_element(locator_type, el)

    def click_all_similar_elements(self, locator_type: str, objs: str, raise_error=True):
        """
        Function used to click on all objects on the page, if any are located. If a given element cannot be clicked
        because it has been obstructed, the function will raise an error by default.
        :param locator_type: Look for objects by means of xpath, id, class, css, etc.
        :param objs: The objects to be located on a given web page.
        :param raise_error: Boolean indicating if error should be raised if a given element cannot be clicked.
        :return: The function returns None.
        """
        fe_objects = self.locators.locate_all_elements(locator_type, objs)
        if fe_objects:
            for el in fe_objects:
                try:
                    if el.is_displayed():
                        self.action.move_to_element(el)
                        el.click()
                        self.action.perform()
                except ElementNotInteractableException as e:
                    if raise_error:
                        raise e
                    if not raise_error:
                        continue

    def wait_url_change(self, url: str):
        """
        The function awaits for the current web url to change from the one provided.
        :param url: The old url that needs to be moved away from.
        :return: The function returns None.
        """
        WebDriverWait(self.browser, 20).until(EC.url_changes(url))

    def wait_for_elements(self, elements: List, time: int):
        """
        Function is used to await for several elements to be present on the web page.
        :param elements: A dictionary of elements that need to be awaited for.
        :param time: The time to wait for each element. By default it's set to 10 seconds.
        :return: The function returns None.
        """
        for el in elements:
            self.locators.wait_element_visible(el['locator_type'], el['obj'], time=time)
