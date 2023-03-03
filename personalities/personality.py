
from abc import abstractmethod


class Personality:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        pass