from code_base.excess_mortality.add_cov_data import CovMortAttrs
from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.get_infostat_dt import DownloadInfostatDT
from code_base.excess_mortality.get_pop_cntr import get_bg_pop
from code_base.excess_mortality.get_population_eu import GetEUPopulation, GetPopUN
from code_base.utils.common_query_params import *

if __name__ == '__main__':
    # TODO: turn into class functions, potentially decorate class to loop.

    # Scrape Infostat for Population Data to load the population for Bulgaria
    c = DownloadInfostatDT('bg_pop_by_age_sex_reg')
    file = c.fetch_infostat_data()
    bg_population_raw = c.rename_and_move_file(file, 'infostat_bg_pop_by_age_sex_reg')

    # Generate Data about Excess mortality for Bulgaria by Region
    years = [2020, 2021]
    cntry = 'BG'

    for year in years:
        bg_mortality = CalcExcessMortality(
            cntry=cntry,
            analyze_year=year
        )
        # Generate data across age groups and sex groups, as a combination between aggregated by age and week.
        for age in age_groups_for_exc_mort:
            for is_age_agg, is_weekly in [[True, True], [True, False], [False, True], [False, False]]:

                mortality = bg_mortality.calc_excess_mort(age_range=age,
                                                          sexes=sex,
                                                          is_weekly=is_weekly,
                                                          is_age_agg=is_age_agg)
                if is_age_agg:
                    merge_on = ['Location', 'Sex']
                else:
                    merge_on = ['Location', 'Age', 'Sex']

                pop_bg = get_bg_pop(file=bg_population_raw, sex=sex, age=age, agg_agg=is_age_agg)

                mortality = bg_mortality.exc_mort_calcs.calc_pop_to_excess_mortality(mortality_df=mortality,
                                                                                     pop_df=pop_bg,
                                                                                     merge_on=merge_on)

                file_name = bg_mortality.get_file_naming_convention(weekly=is_weekly,
                                                                    age_agg=is_age_agg,
                                                                    age_lst=age,
                                                                    sex=sex)

                mort_data_and_info = bg_mortality.set_up_df_for_multisheet_save(mortality)

                bg_mortality.save_multisheet_xlsx(dfs=mort_data_and_info,
                                                  location=bg_mortality.file_loc,
                                                  file_name=file_name)

    # Generate EU population Data
    pop = GetEUPopulation()
    pop.clean_up_df()
    pop_dt = pop.get_agg_sex_cntry_pop(sex=sex)

    # Generate Data about Excess mortality for the EU
    years = [2020, 2021]
    exclude_locations = ['Armenia', 'Albania', 'Germany', 'Georgia', 'United Kingdom']

    for year in years:
        eu_mortality = CalcExcessMortality(
            analyze_year=year,
            exclude_locations=exclude_locations
        )

        # If 90+ then use the population data from the UN since Eurostat's data cuts off at 85+.
        for age in age_groups_for_exc_mort:

            mortality = eu_mortality.calc_excess_mort(age_range=age, sexes=sex)

            if '(90+)' not in age:
                pop_dt = pop.get_agg_sex_cntry_pop(sex=sex, age=age)
            else:
                eu = GetPopUN()
                eu.clean_up_df()
                pop_dt = eu.get_agg_sex_cntry_pop(sex=sex, age=age)

            merge_on = ['Location', 'Sex']

            mortality = eu_mortality.exc_mort_calcs.calc_pop_to_excess_mortality(mortality_df=mortality,
                                                                                 pop_df=pop_dt,
                                                                                 merge_on=merge_on)

            file_name = eu_mortality.get_file_naming_convention(age_lst=age,
                                                                sex=sex)

            mort_data_and_info = eu_mortality.set_up_df_for_multisheet_save(mortality)

            eu_mortality.save_multisheet_xlsx(dfs=mort_data_and_info,
                                              location=eu_mortality.file_loc,
                                              file_name=file_name)
