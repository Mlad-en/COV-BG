from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_pop_bg import get_bg_pop
from code_base.excess_mortality.get_population_eu import GetEUPopulation
from code_base.utils.common_query_params import *

if __name__ == '__main__':
    bg_mortality = CalcExcessMortality(
        cntry='BG'
    )
    pop_bg = get_bg_pop(sex=sex)
    mortality = bg_mortality.get_mortality_df
    bg_mortality.excess_mortality_to_file(mortality, pop_bg)

    for age in age_groups_for_exc_mort:
        bg_mortality.excess_mortality_to_file(mortality, get_bg_pop(age=age, sex=sex), age=age, sex=sex)

    eu_mortality = CalcExcessMortality()
    mortality = eu_mortality.get_mortality_df

    pop = GetEUPopulation()
    pop.clean_up_df()
    pop_dt = pop.get_agg_sex_cntry_pop(sex=sex)
    eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs, sex=sex)

    for age in age_groups_for_exc_mort:
        pop_dt = pop.get_agg_sex_cntry_pop(sex=sex, age=age)
        eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs, sex=sex, age=age)