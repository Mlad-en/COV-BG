from code_base.data_bindings.data_types import EurostatDataSets as DtTp
from code_base.data_cleaners.cleaning_params.eurostat_cleaning_params import EurostatCleaningParams
from code_base.data_cleaners.cleaning_strategies import eurostat_data_cleaning_strategies


class EurostatCleaningConfig:
    AVAILABLE_DATASETS = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY,
        DtTp.MORTALITY_BY_SEX_AGE_REGION,
        DtTp.POP_BY_SEX_AGE_COUNTRY,
    }

    CLEANING_STRATEGIES = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: eurostat_data_cleaning_strategies.EurostatExcessMortalityCleaningStrategy,
        DtTp.MORTALITY_BY_SEX_AGE_REGION:  eurostat_data_cleaning_strategies.EurostatRegionExcessMortalityCleaningStrategy,
        DtTp.POP_BY_SEX_AGE_COUNTRY:       eurostat_data_cleaning_strategies.EurostatEUPopulationCleaningStrategy,
    }

    REPLACE_VALUES = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: [EurostatCleaningParams.REPLACE_VALUES[0],
                                            EurostatCleaningParams.REPLACE_VALUES[1]],

        DtTp.MORTALITY_BY_SEX_AGE_REGION: [EurostatCleaningParams.REPLACE_VALUES[0],
                                           EurostatCleaningParams.REPLACE_VALUES[1]],

        DtTp.POP_BY_SEX_AGE_COUNTRY: [EurostatCleaningParams.REPLACE_VALUES[0],
                                      EurostatCleaningParams.REPLACE_VALUES[1],
                                      EurostatCleaningParams.REPLACE_VALUES[2]],
    }

    SHARED_CLEANING_PARAMS = {
        'split_from_column': EurostatCleaningParams.COLUMN_TO_SPLIT_FROM,
        'split_into_columns': EurostatCleaningParams.COLUMNS_TO_SPLIT_INTO,
        'separator': EurostatCleaningParams.COLUMN_SEPARATOR,
        'filter_cols': EurostatCleaningParams.COLUMNS_TO_RETAIN,
    }

    SHARED_TRANSLATE_VALUES = {
        'Location': EurostatCleaningParams.TRANSLATE_LOCATION_CODE,
        'Sex': EurostatCleaningParams.TRANSLATE_SEX,
        'Age': EurostatCleaningParams.TRANSLATE_AGE
    }


class EurostatCleaningInfo:

    def __init__(self, data_type):

        self._data_type = data_type

    @property
    def _translate_values(self):
        translate_values = {key: value[self._data_type] for key, value in
                            EurostatCleaningConfig.SHARED_TRANSLATE_VALUES.items()}
        return translate_values

    @property
    def _replace_values(self):
        return EurostatCleaningConfig.REPLACE_VALUES[self._data_type]

    @property
    def _specific_params(self):
        return {'translate_values': self._translate_values,
                'replace_values': self._replace_values}

    @property
    def _shared_params(self):
        return {key: value[self._data_type] for (key, value) in EurostatCleaningConfig.SHARED_CLEANING_PARAMS.items()}

    def cleaning_params(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        params = {}
        for dct in (self._shared_params, self._specific_params):
            params.update(dct)
        if kwargs:
            params.update(kwargs)

        return params

    @property
    def cleaning_strategy(self):
        """

        :return:
        """
        return EurostatCleaningConfig.CLEANING_STRATEGIES[self._data_type]
