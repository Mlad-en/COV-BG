import pandas as pd

from code_base.data_output.calc_excess_mortality import CalcExcessMortalityPredicted, CalcEUCountryPop
from code_base.data_source.get_source_data import get_source_data
from code_base.data_bindings.data_types import InfostatDataSets, EurostatDataSets

age = ['Total']
sex = ['Total', 'Male', 'Female']
region = 'BG'
start_week = 10
group_mort = 'slw'
max_year = 2020
years = [2015, 2016, 2017, 2018, 2019, max_year]

mort_type = EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
eu_mort_data = get_source_data(mort_type, analyze_years=years)
excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
calc_mort = excess_mort.calculate(eu_mort_data, age, sex, start_week)

pop_type = EurostatDataSets.POP_BY_SEX_AGE_COUNTRY
eu_pop_data = get_source_data(pop_type, analyze_years=years)
eu_pop = CalcEUCountryPop(data_type=pop_type)
calc_pop = eu_pop.calculate(eu_pop_data, age, sex)

calc_mort = calc_mort.merge(calc_pop, on=['Location', 'Sex'])

calc_mort.to_csv('ensure_correct.csv', index=False, encoding='utf-8-sig')
