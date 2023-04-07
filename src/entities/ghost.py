import random
from typing import TYPE_CHECKING

import pygame

from entities.entity import MovableEntity


if TYPE_CHECKING:
    from engine.level import Level


class Ghost(MovableEntity):
    def __init__(self, level: "Level", x, y) -> None:
        speed = round(level.game.current_level * 0.5 + 2)

        super().__init__(
            level, size=32, speed=speed, image_path="assets/images/ghost.png"
        )

        self.rect = self.image.get_rect(topleft=[x * 40, y * 40])

    def move(self) -> None:
        if random.random() < 0.01:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction = pygame.math.Vector2(dx, dy)

        if self.is_pacman_in_sight():
            dx = self.level.game.pacman.rect.x - self.rect.x
            dy = self.level.game.pacman.rect.y - self.rect.y

            if abs(dx) > abs(dy):
                self.direction = (
                    pygame.math.Vector2(1, 0) if dx > 0 else pygame.math.Vector2(-1, 0)
                )
            else:
                self.direction = (
                    pygame.math.Vector2(0, 1) if dy > 0 else pygame.math.Vector2(0, -1)
                )

        super().move()

    def is_pacman_in_sight(self) -> None:
        sight_distance = 200
        sight_rect = self.rect.inflate(sight_distance, sight_distance)

        if self.direction.x > 0:
            sight_rect.x += self.rect.width
        elif self.direction.x < 0:
            sight_rect.x -= sight_distance

        if self.direction.y > 0:
            sight_rect.y += self.rect.height
        elif self.direction.y < 0:
            sight_rect.y -= sight_distance

        return sight_rect.colliderect(self.level.game.pacman.rect)
