import os
import json
from abc import ABC, abstractmethod
from typing import Any

import pygame


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


class FontManager:
    def __init__(self) -> None:
        self.__size_names = ["small", "default", "large", "huge"]
        self.__fonts: dict[str, pygame.font.Font] = {}

        self.__init_fonts()

    def __init_fonts(self) -> None:
        for size_name, size in zip(self.__size_names, [32, 48, 64, 80]):
            self.__fonts[size_name] = pygame.font.Font(None, size)

    def get(self, name: str) -> pygame.font.Font:
        return self.__fonts[name]

    def get_size_names(self) -> list[str]:
        return self.__size_names


class SettingsManager:
    def __init__(self, settings: AbstractSettings) -> None:
        self.__settings = settings
        self.__font_manager = FontManager()

    def get_size(self) -> tuple[int, int]:
        return self.__settings.get("width", 800), self.__settings.get("height", 800)

    def get_fps(self) -> int:
        return self.__settings.get("fps", 60)

    def get_font(self) -> pygame.font.Font:
        return self.__font_manager.get(self.__settings.get("font", "default"))

    def get_font_size(self) -> str:
        return self.__settings.get("font_size", "default")

    def get_font_size_names(self) -> list[str]:
        return self.__font_manager.get_size_names()

    def get_highscore(self) -> int:
        return self.__settings.get("highscore", 0)

    def get_sound_enabled(self) -> bool:
        return self.__settings.get("sound", True)

    def set(self, key: str, value: Any) -> None:
        self.__settings.set(key, value)

    def save(self) -> None:
        self.__settings.save()

    def load(self) -> None:
        self.__settings.load()
