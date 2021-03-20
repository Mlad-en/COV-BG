from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_population_eu import GetEUPopulation

sex = ['Female', 'Male', 'Total']
age_30_39 = ['(30-34)', '(35-39)']
age_40_64 = ['(40-44)', '(45-49)', '(50-54)', '(55-59)', '(60-64)']
age_65_69 = ['(65-69)']
age_groups = [age_30_39, age_40_64, age_65_69]
exclude_cntrs = ['Serbia', 'Germany']

if __name__ == '__main__':
    # bg_mortaity = CalcExcessMortality(
    #     cntry='BG'
    # )
    # mortality = bg_mortaity.get_mortality_df
    # bg_mortaity.excess_mortality_to_file(mortality)
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(40-44)', '(45-49)', '(50-54)', '(55-59)', '(60-64)'])
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(30-34)', '(35-39)'])
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(65-69)'])

    eu_mortality = CalcExcessMortality()
    mortality = eu_mortality.get_mortality_df
    #
    # pop = GetEUPopulation()
    # pop.clean_up_df()
    # pop_dt = pop.get_age_sex_cntry_pop()
    # eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs)
    #
    # for age in age_groups:
    #     pop_dt = pop.get_age_sex_cntry_pop(sex=sex, age=age)
    #     eu_mortality.excess_mortality_to_file(mortality, pop_dt, sex=sex, age=age, exclude_cntrs=exclude_cntrs)

    eu_mortality.calc_excess_mortality(mortality, add_age=True).to_csv('test.csv')