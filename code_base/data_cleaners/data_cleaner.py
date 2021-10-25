from abc import ABC, abstractmethod


class DataCleaner(ABC):

    def __init__(self, data_to_clean, cleaning_strategy):
        self.data_to_clean = data_to_clean
        self.cleaning_strategy = cleaning_strategy

    @abstractmethod
    def clean_data(self):
        pass


class DataCleanerEurostat(DataCleaner):

    def __init__(self, data_to_clean: str, cleaning_strategy):
        super().__init__(data_to_clean, cleaning_strategy)

    def clean_data(self):
        return self.cleaning_strategy(self.data_to_clean)
