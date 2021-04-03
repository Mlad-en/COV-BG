# This is the official Bulgarian website for Data related to the COVID-19 Pandemic.
EGOV_BG = {
    'main': 'https://data.egov.bg',
    'pages': {

    },
    'api': {
        'path': '/api/getResourceView',
        'api_key': '4f7be417-16cd-492c-bb2a-03a5a66c175a',
        'resource_uri': {
            'general': 'e59f95dd-afde-43af-83c8-ea2916badd19',
            'by_region': 'cb5d7df0-3066-4d7a-b4a1-ac26525e0f0c',
            'by_age_groups': '8f62cfcf-a979-46d4-8317-4e1ab9cbd6a8',
            'by_test_type': '0ce4e9c3-5dfc-46e2-b4ab-42d840caab92'
        }
    }
}

EUROSTAT_POPULATION = {
    'main': 'https://ec.europa.eu',
    'pages': {
    },
    'api': {
        'population': '/eurostat/api/dissemination/sdmx/2.1/data/tps00001/A.JAN.BG?format=CSV&TIME_PERIOD=2020'
    }
}


# Bulgarian Ministry of Health
BG_MH_URL = {
    'main': 'https://www.mh.government.bg',
    'pages': {
        'news': {
            'landing_page': '/novini/aktualno/',
            'page_params': {'start_date': 'start_date', 'end_date': 'end_date', 'category': 'category'}
        },
    }
}