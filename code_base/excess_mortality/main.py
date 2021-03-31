from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_pop_cntr import get_bg_pop
from code_base.excess_mortality.get_population_eu import GetEUPopulation, GetPopUN
from code_base.utils.common_query_params import *

if __name__ == '__main__':

    # Generate Data about Excess mortality for Bulgaria by Region
    bg_mortality = CalcExcessMortality(
        cntry='BG'
    )
    pop_bg = get_bg_pop(sex=sex)
    mortality = bg_mortality.get_mortality_df
    bg_mortality.excess_mortality_to_file(mortality, pop_bg, sex=sex)

    for age in age_groups_for_exc_mort:
        bg_mortality.excess_mortality_to_file(mortality, get_bg_pop(age=age, sex=sex), age=age, sex=sex)

    # Generate Data about Excess mortality for the EU
    eu_mortality = CalcExcessMortality()
    mortality = eu_mortality.get_mortality_df

    pop = GetEUPopulation()
    pop.clean_up_df()
    pop_dt = pop.get_agg_sex_cntry_pop(sex=sex)
    eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs, sex=sex)

    # If 90+ then use the population data from the UN since Eurostat's data cuts off at 85+.
    for age in age_groups_for_exc_mort:
        if '(90+)' not in age:
            pop_dt = pop.get_agg_sex_cntry_pop(sex=sex, age=age)
        else:
            eu = GetPopUN()
            eu.clean_up_df()
            pop_dt = eu.get_agg_sex_cntry_pop(sex=sex, age=age)
        eu_mortality.excess_mortality_to_file(mortality, pop_dt, exclude_cntrs=exclude_cntrs, sex=sex, age=age)