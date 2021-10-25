DECODE_BUTTONS = {
    'request': {
        'en': 'Send',
        'bg': 'Заяви',
    },
    'download': {
        'en': 'Download',
        'bg': 'Изтегли',
    }
}

SWITCH_TO_ENGLISH = {
    'locator_type': 'xpath',
    'obj': '//*[text()="EN"]',
}

SWITCH_TO_BULGARIAN = {
        'locator_type': 'xpath',
        'obj': '//*[text()="БГ"]',
    }

CHECK_ALL_PARENT_CHECKBOXES = {
    'locator_type': 'xpath',
    'objs': '//*/thead/tr/th[1]/div/div[2]/span',
}

UNCHECK_SPECIFIC_CHECKBOXES = {
    'locator_type': 'xpath',
    'objs': '//span[text()="REPLACE_TEXT"]/../../td[1]/div/div/span'
}

UNCHECK_NUTS2_REGIONS = {
    'locator_type': 'xpath',
    'objs': '//td[text()=4]/../td[1]/div/div/span'
}

REQUEST_BUTTON = {
    'locator_type': 'xpath',
    'obj': '//*[text()="REPLACE_TEXT"]'
}

DOWNLOAD_FILE_TYPE = {
    'locator_type': 'xpath',
    'obj': '//*[text()="XLSX"]'
}

FIND_TEXT = {
        'locator_type': 'xpath',
        'obj': '//*[text()="REPLACE_TEXT"]',
    }