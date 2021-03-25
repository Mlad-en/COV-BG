from code_base.pyll.url_constants import BG_NSI_URL, CZ_CZSO_URL

DECODE_WHO_GENDER_VARS = {
    'BTSX': 'Total',
    'MLE': 'Male',
    'FMLE': 'Female',
}

DECODE_WHO_AGE_RANGES = {
    'AGE1-4': '(0-4)',
    'AGE5-9': '(5-9)',
    'AGE10-14': '(10-14)',
    'AGE15-19': '(15-19)',
    'AGE20-24': '(20-24)',
    'AGE25-29': '(25-29)',
    'AGE30-34': '(30-34)',
    'AGE35-39': '(35-39)',
    'AGE40-44': '(40-44)',
    'AGE45-49': '(45-49)',
    'AGE50-54': '(50-54)',
    'AGE55-59': '(55-59)',
    'AGE60-64': '(60-64)',
    'AGE65-69': '(65-69)',
    'AGE70-74': '(70-74)',
    'AGE75-79': '(75-79)',
    'AGE80-84': '(80-84)',
    'AGE85PLUS': '(85-89)',
}


# __countries life expencancy bindings used for the country_dt-level life expectancy function
LIFE_EXPECTANCY_DATA = {
    'Bulgaria': {
        'partial': False,
        'lf_ex_clean': 'bg_life_expectancy',
        'sheet_name': '2017-2019',
        'url_dict': BG_NSI_URL,
        'page_file': 'files',
        'pf_name': 'life_expectancy',
        'columns': ['Unnamed: 0', 'Unnamed: 8', 'Unnamed: 9'],
        'rename_columns': ['Age', 'Male', 'Female'],
        'start_index': ['Unnamed: 0', 'Общо за страната'],
        'end_index': ['Unnamed: 0', '100+'],
    },
    'Czech Republic-MEN': {
        'partial': True,
        'partial_type': 'men',
        'lf_ex_clean': 'cz_life_expectancy_men',
        'url_dict': CZ_CZSO_URL,
        'page_file': 'files',
        'pf_name': 'life_expectancy_men',
        'columns': ['2019', 'Unnamed: 9'],
        'rename_columns': ['Age', 'Male'],
        'start_index': ['2019', 'věk (x) age'],
    },
    'Czech Republic-WOMEN': {
        'partial': True,
        'partial_type': 'women',
        'lf_ex_clean': 'cz_life_expectancy_women',
        'url_dict': CZ_CZSO_URL,
        'page_file': 'files',
        'pf_name': 'life_expectancy_women',
        'columns': ['2019', 'Unnamed: 9'],
        'rename_columns': ['Age', 'Female'],
        'start_index': ['2019', 'věk (x) age'],
    }
}

LIFE_EXPECTANCY_DATA_PACKAGED = {
    'Bulgaria': [LIFE_EXPECTANCY_DATA['Bulgaria']],
    'Czechia': [
        LIFE_EXPECTANCY_DATA['Czech Republic-MEN'],
        LIFE_EXPECTANCY_DATA['Czech Republic-WOMEN'],
                ]
}

LIST_LIFE_EXP_DT_COUNTRIES = [country for country in LIFE_EXPECTANCY_DATA_PACKAGED.keys()]