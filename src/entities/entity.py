import pygame

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from level import Level


class IEntity(ABC):
    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass


class Entity(IEntity, pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, level: "Level") -> None:
        super().__init__()

        self.level = level

    def draw(self, screen: pygame.Surface) -> None:
        """
        Відображає сутність на екрані.
        """

        screen.blit(self.image, self.rect)

    def update(self) -> None:
        pass


class MovableEntity(Entity):
    def __init__(self, level: "Level", size: int, speed: int) -> None:
        super().__init__(level)

        self.size = size
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)

    def move(self) -> None:
        """
        Переміщає сутність у вказаному напрямку.
        """

        new_position = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_position):
            self.rect = new_position

    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Перевіряє чи не виникла колізія з стіною.
        """

        for wall in self.level.walls:
            if wall.rect.colliderect(rect):
                return True

        return False
