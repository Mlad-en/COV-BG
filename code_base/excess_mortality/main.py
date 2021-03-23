from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_population_eu import GetEUPopulation
from code_base.excess_mortality.common_query_params import *
if __name__ == '__main__':
    # bg_mortaity = CalcExcessMortality(
    #     cntry='BG'
    # )
    # mortality = bg_mortaity.get_mortality_df
    # bg_mortaity.excess_mortality_to_file(mortality)
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(40-44)', '(45-49)', '(50-54)', '(55-59)', '(60-64)'])
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(30-34)', '(35-39)'])
    # bg_mortaity.excess_mortality_to_file(mortality, sex=['Female', 'Male'], age=['(65-69)'])
    #
    eu_mortality = CalcExcessMortality()
    mortality = eu_mortality.get_mortality_df

    pop = GetEUPopulation()
    pop.clean_up_df()
    pop_dt = pop.get_age_sex_cntry_pop(sex=sex)
    eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs, sex=sex)

    for age in age_groups_for_exc_mort:
        pop_dt = pop.get_age_sex_cntry_pop(sex=sex, age=age)
        eu_mortality.calc_excess_mortality(eu_mortality.clean_eu_data(mortality, exclude_cntrs), add_age=True)