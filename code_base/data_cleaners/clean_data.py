from code_base.data_bindings.data_types import InfostatDataSets, EurostatDataSets
from code_base.data_cleaners.cleaning_info.eurostat_cleaning_info import EurostatCleaningInfo
from code_base.data_cleaners.cleaning_info.infostat_cleaning_info import InfostatCleaningInfo


def clean_data(data_type, data, **params):
    mapping = {
        InfostatDataSets: InfostatCleaningInfo,
        EurostatDataSets: EurostatCleaningInfo,
    }

    data_type_class = data_type.__class__
    data_type_cleaning = mapping.get(data_type_class)
    if not data_type_cleaning:
        raise ValueError(f'Could Not find a data cleaning info for data type: {str(data_type)}')

    data_cleaning_info = data_type_cleaning(data_type)
    cleaning_params = data_cleaning_info.cleaning_params(**params)
    cleaning_strategy = data_cleaning_info.cleaning_strategy(data, **cleaning_params)
    return cleaning_strategy.clean_data()
