import os
import json
from abc import ABC, abstractmethod
from typing import Any


class AbstractSettings(ABC):
    @abstractmethod
    def get(self, key: str, default: Any) -> None:
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    def save(self):
        ...

    @abstractmethod
    def load(self) -> None:
        ...

class JsonSettings(AbstractSettings):
    def __init__(self, path: str) -> None:
        self.__path = path
        self.__data = {}

    def get(self, key: str, default: Any) -> Any:
        return self.__data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.__data[key] = value

    def save(self) -> None:
        with open(self.__path, "w") as file:
            json.dump(self.__data, file, indent=4)

    def load(self) -> None:
        if os.path.exists(self.__path):
            with open(self.__path, "r") as file:
                self.__data = json.load(file)