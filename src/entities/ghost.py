import random
from typing import TYPE_CHECKING

import pygame

from entities.entity import MovableEntity


if TYPE_CHECKING:
    from engine.level import Level


class Ghost(MovableEntity):
    def __init__(self, level: "Level", x, y) -> None:
        super().__init__(level, size=32, speed=2, image_path="assets/images/ghost.png")

        self.rect = self.image.get_rect(topleft=[x * 40, y * 40])

    def move(self) -> None:
        if random.random() < 0.01:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction = pygame.math.Vector2(dx, dy)

        super().move()
