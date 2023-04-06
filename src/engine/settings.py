from abc import ABC, abstractmethod
import toml

class ISettings(ABC):
    @abstractmethod
    def __getitem__(self, key: str):
        pass

class Settings(ISettings):
    def __init__(self, config_file="settings.toml"):
        self.config = toml.load(config_file)

    def __getitem__(self, key: str):
        return self.config[key]