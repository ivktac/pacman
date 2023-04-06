import os
from typing import TYPE_CHECKING

import pygame

from entities.food import Food
from entities.wall import Wall
from entities.ghost import Ghost

if TYPE_CHECKING:
    from game import Game


class Level:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.settings = game.settings

        self.walls = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

    def reset(self) -> None:
        """
        Скидає стан рівня до початкового.
        """

        self.walls.empty()
        self.foods.empty()
        self.ghosts.empty()

    def load(self, level_number: int) -> None:
        """
        Завантажує дані рівня та створює відповідні об’єкти.
        """

        self.reset()

        filename = os.path.join(
            self.settings["levels"]["path"], f"{level_number}.txt"
        )
        with open(filename, "r") as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                match tile:
                    case "=":
                        wall = Wall(self, x, y)
                        self.walls.add(wall)
                    case "P":
                        size = self.settings["wall"]["size"]
                        self.game.pacman.set_position(x * size, y * size)
                    case "*":
                        food = Food(self, x, y)
                        self.foods.add(food)
                    case "G":
                        ghost = Ghost(self, x, y)
                        self.ghosts.add(ghost)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.
        """

        self.ghosts.draw(screen)
        self.game.pacman.draw(screen)
        self.walls.draw(screen)
        self.foods.draw(screen)

    def update(self) -> None:
        """
        Оновлює стан рівня, як-от положення та взаємодію усіх об’єктів на рівні.
        """

        self.game.pacman.update()
        self.ghosts.update()

    def restart(self) -> None:
        """
        Перезавантажує рівень.
        """

        self.walls.empty()
        self.foods.empty()
        self.ghosts.empty()


    def is_completed(self) -> bool:
        """
        Повертає True, якщо рівень завершено, інакше False.
        """

        return len(self.foods) == 0