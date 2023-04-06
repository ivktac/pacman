from abc import ABC, abstractmethod
import json
import toml


class ISettings(ABC):
    @abstractmethod
    def __getitem__(self, key: str):
        ...

    @abstractmethod
    def __setitem__(self, key: str, value):
        ...


class TomlSettings(ISettings):
    def __init__(self, config_file="settings.toml"):
        self.config = toml.load(config_file)

    def __getitem__(self, key: str):
        return self.config[key]

    def __setitem__(self, key: str, value):
        self.config[key] = value


class JsonSettings(ISettings):
    def __init__(self, config_file="settings.json"):
        self.config = json.load(open(config_file))

    def __getitem__(self, key: str):
        return self.config[key]

    def __setitem__(self, key: str, value):
        self.config[key] = value
