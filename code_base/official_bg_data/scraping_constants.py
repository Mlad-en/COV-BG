MH_TITLE_ARTICLE_PATTERN = r'^[1-9]+.+(корона|COVID|коронавирусна)'

MH_SPIT_BY_GENDER_ARTICLE_PATTERN = r'(мъж|жена|бебе)'

MH_RAW_ARTICLE_TEXT_COLUMNS = ['title', 'link', 'date', 'article_text']

MH_PER_PERSON_COLUMNS = [
    'date', 'person_data_raw', 'gender',
    'age', 'no_comorbidity', 'diabetes',
    'cardiovascular', 'neurological', 'pulmonary',
    'oncological', 'hepatological', 'pneumonia',
    'unknown', 'obeasity',
]

MH_PER_PERSON_COMORBIDITY = {
    'diabetes': ['диабет'],
    'cardiovascular': ['сърдеч', ' инфаркт', 'инсулт', 'исхемич', 'хематологич', 'съдов', 'артериална хипертония'],
    'neurological': ['неврологич', 'деменция', 'алцхаймер'],
    'pulmonary': ['белодроб', 'ХОББ', 'хронична обструктивна белодробна болест', 'астма'],
    'pneumonia': ['пневмония'],
    'oncological': ['онкологич', 'рак', 'имунен дефицит'],
    'hepatological': ['чернодроб'],
    'nephrological': ['бъбре'],
    'obeasity': ['затлъстяване'],
    'unknown': ['неуточнено', 'множество придружаващи заболявания', 'множество заболявания'],
}

MH_PER_PERSON_AGE_PATTERN = r'[\d]+'
