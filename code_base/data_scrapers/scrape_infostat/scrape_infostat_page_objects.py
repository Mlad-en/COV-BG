from code_base.data_bindings.sex_translations import INFOSTAT_BG_SEX_BINDINGS, SEX_BINDINGS

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

WAIT_FOR_DEMO_ELEMENTS_BG = [
    {'locator_type': FIND_TEXT['locator_type'],
     'obj': FIND_TEXT['obj'].replace('REPLACE_TEXT', INFOSTAT_BG_SEX_BINDINGS.FEMALE)
     },
    {'locator_type': FIND_TEXT['locator_type'],
     'obj': FIND_TEXT['obj'].replace('REPLACE_TEXT', INFOSTAT_BG_SEX_BINDINGS.MALE)
     },
]

WAIT_FOR_DEMO_ELEMENTS_EN = [
    {'locator_type': FIND_TEXT['locator_type'],
     'obj': FIND_TEXT['obj'].replace('REPLACE_TEXT', SEX_BINDINGS.FEMALE)
     },
    {'locator_type': FIND_TEXT['locator_type'],
     'obj': FIND_TEXT['obj'].replace('REPLACE_TEXT', SEX_BINDINGS.MALE)
     },
]