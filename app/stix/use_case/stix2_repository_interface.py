from abc import abstractmethod

from stix2 import Indicator


class IStix2Repository:

    @abstractmethod
    def save_indicator(self, sdo_dict: dict):
        pass

    @abstractmethod
    def find_indicator_by_pattern(self, pattern) -> Indicator | None:
        pass

    @abstractmethod
    def save_smo(self, smo_dict: dict):
        pass
