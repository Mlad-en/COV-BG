class COLUMN_HEADING_CONSTS:
    SEX = 'Sex'
    AGE = 'Age'
    LOCATION = 'Location'
    YEAR_2020 = '2020'
    YEAR_2021 = '2021'
    MORTALITY = 'Mortality'
    POPULATION = 'Population'
    LIFE_EXPECTANCY = 'Life_Expectancy'
    YEAR = 'Year'
    WEEK = 'Week'

    STANDARD_DEVIATION = 'STANDARD_DEVIATION'
    Z_SCORE = 'Z-Score(95%)'
    CONFIDENCE_INTERVAL = 'Conf_interval'
    IS_SIGNIFICANT = 'SIGNIFICANT'

    MEAN_OR_EXPECTED_MORTALITY = 'Mean/Expected_' + MORTALITY
    LB_MEAN_MORTALITY = 'Lower_bound_' + MEAN_OR_EXPECTED_MORTALITY
    UB_MEAN_MORTALITY = 'Upper_bound_' + MEAN_OR_EXPECTED_MORTALITY
    MEAN_MORTALITY_DECORATED = MEAN_OR_EXPECTED_MORTALITY + ' ±'

    EXCESS_MORTALITY_BASE = 'Excess_mortality'
    EXCESS_MORTALITY_MEAN = 'Excess_mortality'
    EXCESS_MORTALITY_FLUCTUATION = EXCESS_MORTALITY_BASE + '_fluctuation'
    EXCESS_MORTALITY_DECORATED = EXCESS_MORTALITY_BASE + ' ±'

    EXCESS_MORTALITY_PER_100_000 = 'Excess_mortality_per_100_000'
    EXCESS_MORTALITY_PER_100_000_FLUCTUATION = 'Excess_mortality_per_100_000' + '_fluctuation'
    EXCESS_MORTALITY_PER_100_000_DECORATED = EXCESS_MORTALITY_PER_100_000 + ' ±'

    P_SCORE = 'P_Score'
    P_SCORE_FLUCTUATION = P_SCORE + '_fluctuation'
    P_SCORE_DECORATED = P_SCORE + ' ±'

    PYLL_MEAN = 'PYLL_mean'
    PYLL_FLUCTUATION = 'PYLL_fluctuation'
    PYLL_AVG_MEAN = 'PYLL_average_mean'
    PYLL_AVG_FLUC = 'PYLL_fluctuation'
    PYLL_STD_MEAN = 'PYLL_STD_MEAN'
    PYLL_STD_FLUC = 'PYLL_STD_FLUC'
