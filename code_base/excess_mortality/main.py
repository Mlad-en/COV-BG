from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality

if __name__ == '__main__':
    c = CalcExcessMortality(
        cntry='BG'
    )
    mortality = c.get_mortality_df
    c.excess_mortality_to_file(mortality)
    # c.to_file(mortality, sex=['Female', 'Male'], age=['(40-44)', '(45-49)', '(50-54)', '(55-59)', '(60-64)'])
