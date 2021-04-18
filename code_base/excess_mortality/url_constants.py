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

# National Statistics Institute Bulgaria (NSI)
# NSI implemented a CloudFlare protection and scraping that website is no longer possible.
NSI_DATA = {
    'main': 'https://www.nsi.bg',
    'pages': {
        'bg_pop_by_age_sex_reg':
            '/en/content/6708/population-districts-age-place-residence-and-sex'
    }
}

# Information System of the National Statistical Institute. Used for historical data.
# NSI implemented a CloudFlare protection and scraping that website is no longer possible. Using this one instead.
INFOSTAT_DATA = {
    'main': 'https://infostat.nsi.bg',
    'pages': {
        'bg_pop_by_age_sex_reg': '/infostat/pages/reports/query.jsf?x_2=1168',
        'mortality_by_age_sex_mun': '/infostat/pages/reports/query.jsf?x_2=1033',
        'avg_life_expectancy_by_sex': '/infostat/pages/reports/query.jsf?x_2=41',
        'life_expectancy_by_sex': '/infostat/pages/reports/query.jsf?x_2=230',
        'population_by_municipality': '/infostat/pages/reports/query.jsf?x_2=1062'
    }
}