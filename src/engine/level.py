import os
import pygame

from entities.player import Player
from entities.food import Food
from entities.wall import Wall
from entities.ghost import Ghost


class Level(pygame.sprite.Group):
    def __init__(self, number: int, player: Player) -> None:
        super().__init__()

        self.__player = player

        self.__number = number

        self.load()

    @property
    def player(self) -> Player:
        return self.__player

    def load(self) -> None:
        filename = f"assets/levels/{self.__number}.txt"
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Level {self.__number} not found")

        with open(f"assets/levels/{self.__number}.txt", "r") as file:
            data = file.read().splitlines()

        self.empty()

        self.create(data)

    def create(self, data) -> None:
        for y, line in enumerate(data):
            for x, tile in enumerate(line):
                match tile:
                    case "=":
                        self.add(Wall(x, y))
                    case "P":
                        self.__player.respawn(x * 40 + 5, y * 40 + 5)
                    case "*":
                        self.add(Food(x, y, "food"))
                    case "C":
                        self.add(Food(x, y, "cherry"))
                    case "S":
                        self.add(Food(x, y, "blueberry"))
                    case "G":
                        speed = round(self.__number * 0.25 + 2)
                        self.add(Ghost(x, y, speed))

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.sprites():
            sprite.draw(screen)

        self.__player.draw(screen)

    def update(self) -> None:
        for sprite in self.sprites():
            sprite.update(self)

        self.__player.update(self)

    def is_completed(self) -> bool:
        return not any(isinstance(entity, Food) for entity in self.sprites())
