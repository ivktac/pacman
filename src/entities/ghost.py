from typing import TYPE_CHECKING
import pygame
from entity import MovableEntity


if TYPE_CHECKING:
    from level import Level


class Ghost(MovableEntity):
    def __init__(self, level: "Level", size: int, speed: int) -> None:
        size = level.settings.ghost["size"]
        speed = level.settings.ghost["speed"]

        super().__init__(level, size, speed)

        image_path = level.settings.ghost["image"]
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.rect = self.image.get_rect()