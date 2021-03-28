EUROSTAT_DATA = {
    'main': 'https://ec.europa.eu',
    'pages': {
        'bulk_data': '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?dir=data',
        'excess_mortality_by_sex_age_country':
            '/eurostat/databrowser/view/demo_r_mwk_05/default/table?lang=en',
        'excess_mortality_by_sex_age_nuts3':
            '/eurostat/databrowser/view/demo_r_mweek3/default/table?lang=en',
        'europe_population_by_age_and_sex':
            '/eurostat/databrowser/view/demo_pjangroup/default/table?lang=en'
    },
    'files': {
        'excess_mortality_by_sex_age_country':
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mwk_05.tsv.gz',
        'excess_mortality_by_sex_age_nuts3':
            '/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fdemo_r_mweek3.tsv.gz',
        'europe_population_by_age_and_sex':
            '/eurostat/api/dissemination/sdmx/2.1/data/demo_pjangroup/?&format=CSV'
    },
}

# Czechia Covid-19 stats website
CZ_COV_URL = {
    'main': 'https://onemocneni-aktualne.mzcr.cz',
    'pages': {
        'api_list': '/api/v2/covid-19'
    },
    'files': {
        'mortality_by_age_gender': '/api/v2/covid-19/umrti.csv'
    }
}
