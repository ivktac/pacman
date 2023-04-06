from abc import ABC, abstractmethod
import json
import toml


class ISettings(ABC):
    @abstractmethod
    def save(self):
        ...

    @abstractmethod
    def __getitem__(self, key: str):
        ...

    @abstractmethod
    def __setitem__(self, key: str, value):
        ...


class TomlSettings(ISettings):
    def __init__(self, config_file="settings.toml"):
        self.__file = config_file
        self.__config = toml.load(config_file)

    def save(self):
        toml.dump(self.__config, open(self.__file, "w"))

    def __getitem__(self, key: str):
        return self.__config[key]

    def __setitem__(self, key: str, value):
        self.__config[key] = value


class JsonSettings(ISettings):
    def __init__(self, config_file="settings.json"):
        self.__file = config_file
        self.config = json.load(open(config_file))

    def save(self):
        json.dump(self.config, open(self.__file, "w"))

    def __getitem__(self, key: str):
        return self.config[key]

    def __setitem__(self, key: str, value):
        self.config[key] = value
