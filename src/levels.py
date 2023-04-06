import os
from typing import TYPE_CHECKING

import pygame
from entities import Food, Wall

if TYPE_CHECKING:
    from game import Game


class Level:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.settings = game.settings

        self.current_level = 1

        self.walls = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()

    def load_level(self, level_number: int) -> None:
        """
        Завантажує дані рівня та створює відповідні об’єкти.
        """

        filename = os.path.join(self.settings.levels["path"], f"{level_number}.txt")
        with open(filename, "r") as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                match tile:
                    case "=":
                        wall = Wall(self, x, y)
                        self.walls.add(wall)
                    case "P":
                        self.place_player(x, y)
                    case '*':
                        food = Food(self, x, y)
                        self.foods.add(food)

    def place_player(self, x, y) -> None:
        """
        Поміщає гравця на початкову позицію.
        """

        size = self.settings.wall["size"]
        self.game.pacman.set_position(x * size, y * size)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.
        """

        self.game.pacman.draw(screen)
        self.walls.draw(screen)
        self.foods.draw(screen)

    def update(self) -> None:
        """
        Оновлює стан рівня, як-от положення та взаємодію усіх об’єктів на рівні.
        """

        self.game.pacman.update()
