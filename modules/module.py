
# Abstract class for a module

from abc import abstractmethod


class Module:

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        pass

    @abstractmethod
    def get_triggers(self) -> list:
        pass

    @abstractmethod
    def get_response(self, message: str) -> str:
        pass