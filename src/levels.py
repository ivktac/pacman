from typing import TYPE_CHECKING

import pygame
from entities import Wall

if TYPE_CHECKING:
    from game import Game


class Level:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.settings = game.settings

        self.current_level = 1

        self.walls = pygame.sprite.Group()

    def load_level(self, level_number: int) -> None:
        """
            Завантажує дані рівня та створює відповідні об’єкти.
        """

        wall_data = [
            {"x": 0, "y": 0, "width": 640, "height": 20},  # Top border
            {"x": 0, "y": 460, "width": 640, "height": 20},  # Bottom border
            {"x": 0, "y": 0, "width": 20, "height": 480},  # Left border
            {"x": 620, "y": 0, "width": 20, "height": 480},  # Right border
        ]

        for wall_info in wall_data:
            wall = Wall(self, **wall_info)
            self.walls.add(wall)

    def draw(self, screen: pygame.Surface) -> None:
        """
            Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.
        """

        self.walls.draw(screen)
        self.game.pacman.draw(screen)

    def update(self) -> None:
        """
            Оновлює стан рівня, як-от положення та взаємодію усіх об’єктів на рівні.
        """

        self.game.pacman.update()
