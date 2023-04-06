import random
from typing import TYPE_CHECKING

import pygame

from entities.entity import Entity

if TYPE_CHECKING:
    from level import Level


class Food(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        super().__init__(level)

        self.size = self.level.settings["food"]["size"]
        wall_size = self.level.settings["wall"]["size"]

        self.color = self.level.settings["colors"]["food"]

        self.image = pygame.Surface(
            [self.size, self.size], pygame.SRCALPHA, 32
        ).convert_alpha()

        pygame.draw.circle(
            self.image, self.color, (self.size // 2, self.size // 2), self.size // 2
        )

        self.rect = self.image.get_rect(
            topleft=[x * wall_size + self.size, y * wall_size + self.size]
        )

        self.points = random.randint(1, 10)
