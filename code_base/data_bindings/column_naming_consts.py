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

    MEAN_MORTALITY = 'Mean_' + MORTALITY
    LB_MEAN_MORTALITY = 'Lower_bound_' + MEAN_MORTALITY
    UB_MEAN_MORTALITY = 'Upper_bound_' + MEAN_MORTALITY
    MEAN_MORTALITY_DECORATED = MEAN_MORTALITY + ' ±'

    EXCESS_MORTALITY = 'Excess_mortality'
    EXCESS_MORTALITY_MEAN = EXCESS_MORTALITY + '_Mean'
    EXCESS_MORTALITY_FLUCTUATION = EXCESS_MORTALITY + '_fluctuation'
    EXCESS_MORTALITY_DECORATED = EXCESS_MORTALITY + ' ±'

    EXCESS_MORTALITY_PER_100_000 = 'Excess_mortality_per_100_000'
    EXCESS_MORTALITY_PER_100_000_FLUCTUATION = 'Excess_mortality_per_100_000'  + '_fluctuation'

    P_SCORE = 'P_Score'
    P_SCORE_FLUCTUATION = P_SCORE + '_fluctuation'
    P_SCORE_DECORATED = P_SCORE + ' ±'
