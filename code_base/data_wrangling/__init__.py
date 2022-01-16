from code_base.data_bindings import data_types
from code_base.data_source.get_source_data import get_source_data

if __name__ == '__main__':
    from code_base.data_wrangling.wrangling_strategies.local_file_wrangling_strategies import \
        ItalyPopulationWranglingStrategy
    # data = get_source_data(data_types.LocalDataSets.Italy_Population)
    # wrangle_data = ItalyPopulationWranglingStrategy(['(85-89)', '(90+)'], ['Total'])
    # group_df = wrangle_data.group_data(data)
    # filtered_df = wrangle_data.filter_data(group_df)
    # filtered_df["LOCATION"] = 'Italy'
    #
    # data = get_source_data(data_types.LocalDataSets.Italy_Population)

    exc_mort = get_source_data(data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY, analyze_years=[2015, 2016, 2017, 2018, 2019, 2020])
