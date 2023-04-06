import random
from typing import TYPE_CHECKING

import pygame

from entities.entity import MovableEntity


if TYPE_CHECKING:
    from level import Level


class Ghost(MovableEntity):
    def __init__(self, level: "Level", x, y) -> None:
        size = level.settings["ghost"]["size"]
        wall_size = level.settings["wall"]["size"]
        speed = level.settings["ghost"]["speed"]
        image_path = level.settings["ghost"]["image"]

        super().__init__(level, size=size, speed=speed, image_path=image_path)

        self.rect = self.image.get_rect(topleft=[x * wall_size, y * wall_size])

    def move(self) -> None:
        """
        Переміщає привидів.
        """

        if random.random() < 0.01:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction = pygame.math.Vector2(dx, dy)

        super().move()