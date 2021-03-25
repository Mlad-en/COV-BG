
WHO_DATA = {
    'main': 'https://apps.who.int',
    'pages': {
        'life_tables': '/gho/data/node.imr.LIFE_0000000035?lang=en'
    },
    'api': {
        'life_tables_europe': '/gho/athena/data/GHO/LIFE_0000000035.csv?filter=REGION:###REGION###;YEAR:###YEAR###'
    }
}
# Bulgarian National Statistics Institute
BG_NSI_URL = {
    'main': 'https://www.nsi.bg',
    'pages': {
        'mortality_per_week': '/bg/node/18121/',
        'life_expectancy':
            '/bg/content/3018/смъртност-и-средна-продължителност-на-предстоящия-живот-на-населението-по-местоживеене',
        'population_by_region':
        '/en/content/6704/population-districts-municipalities-place-residence-and-sex'
    },
    'files': {
        'mortality_per_week': '/bg/node/18121/',
        'life_expectancy': '/sites/default/files/files/data/timeseries/Pop_3.1_tab_mortality_DR.xls',
        'population_by_region': '/sites/default/files/files/data/timeseries/Pop_6.1.1_Pop_DR_EN.xls'
    }
}
# Czechia National Statistics Office
CZ_CZSO_URL = {
    'main': 'https://www.czso.cz',
    'pages': {
        'life_expectancy':
            '/csu/czso/umrtnostni-tabulky-za-cr-regiony-soudrznosti-a-kraje-2018-2019'
    },
    'files': {
        'life_expectancy_men':
            '/documents/10180/121739354/1300632001.xlsx/2056ff1b-2574-4af3-ac47-160b62b2129b?version=1.1',
        'life_expectancy_women':
            '/documents/10180/121739354/1300632002.xlsx/eda89506-30fa-46e1-b3db-eda58575ba78?version=1.1'
    }
}
