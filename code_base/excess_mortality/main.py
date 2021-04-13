from code_base.excess_mortality.add_cov_data import CovMortAttrs
from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_infostat_dt import DownloadInfostatDT
from code_base.excess_mortality.get_pop_cntr import get_bg_pop
from code_base.excess_mortality.get_population_eu import GetEUPopulation, GetPopUN
from code_base.utils.common_query_params import *

if __name__ == '__main__':
    # Scrape Infostat for Population Data to load the population for Bulgaria
    c = DownloadInfostatDT('bg_pop_by_age_sex_reg')
    file = c.fetch_infostat_data()
    bg_population_raw = c.rename_and_move_file(file, 'infostat_bg_pop_by_age_sex_reg')
    pop_bg = get_bg_pop(file=bg_population_raw, sex=sex)

    # Generate Data about Excess mortality for Bulgaria by Region
    bg_mortality = CalcExcessMortality(
        cntry='BG'
    )
    mortality = bg_mortality.get_mortality_df

    # Generate by age group excess mortality; data is not summed across age groups.
    bg_mortality.save_df_to_file(bg_mortality.calc_excess_mortality(mortality, add_age=True),
                                 bg_mortality.file_loc,
                                 'bg_total_excess_mortality_by_loc_sex_age',
                                 method='excel')

    # Generate agg excess mortality.
    files = bg_mortality.excess_mortality_to_file(mortality, pop_bg, sex=sex)
    bg_mort = CovMortAttrs()
    all_sx_official_exc_mort = bg_mort.add_exces_official_dt(exc_mort_total_loc=files['total'])
    all_mort = bg_mort.add_test_pos_data_df(all_sx_official_exc_mort)
    bg_mort.save_df_to_file(df=all_mort,
                            location=bg_mort.output_loc,
                            file_name="TOTAL_BG_Total_excess_mortality_off_mortality_testing_2020")

    for age in age_groups_for_exc_mort:
        bg_mortality.excess_mortality_to_file(mortality, get_bg_pop(file=bg_population_raw,
                                                                    age=age,
                                                                    sex=sex), age=age, sex=sex)

    # Generate population Data
    pop = GetEUPopulation()
    pop.clean_up_df()
    pop_dt = pop.get_agg_sex_cntry_pop(sex=sex)

    # Generate Data about Excess mortality for the EU
    eu_mortality = CalcExcessMortality()
    mortality = eu_mortality.get_mortality_df
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