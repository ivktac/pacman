from typing import TYPE_CHECKING

import pygame

from entities.entity import Entity

if TYPE_CHECKING:
    from level import Level


class Wall(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        super().__init__(level)

        self.size = self.level.settings.wall["size"]

        image_path = self.level.settings.wall["image"]
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, [self.size, self.size])

        self.rect = self.image.get_rect(topleft=[x * self.size, y * self.size])
