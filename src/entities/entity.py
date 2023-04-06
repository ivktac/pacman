import pygame

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.level import Level


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

    def __init__(
        self,
        level: "Level",
        size: int | None = None,
        image_path: str | None = None,
        color: str | None = None,
    ) -> None:
        super().__init__()

        self.level = level

        if size is not None:
            self.size = size
            if image_path is not None:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
            elif color is not None:
                self.image = pygame.Surface(
                    [self.size, self.size], pygame.SRCALPHA, 32
                ).convert_alpha()
                pygame.draw.circle(
                    self.image, color, (self.size // 2, self.size // 2), self.size // 2
                )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Відображає сутність на екрані.
        """

        screen.blit(self.image, self.rect)

    def update(self) -> None:
        pass


class MovableEntity(Entity):
    def __init__(self, level: "Level", size: int, speed: int, image_path: str) -> None:
        super().__init__(level, size=size, image_path=image_path)

        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)

    def update(self) -> None:
        self.move()

    def move(self) -> None:
        """
        Переміщає сутність у вказаному напрямку.
        """

        new_position = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_position):
            self.rect = new_position

        self.wrap_around()

    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Перевіряє чи не виникла колізія з стіною.
        """

        for wall in self.level.walls:
            if wall.rect.colliderect(rect):
                return True

        return False

    def wrap_around(self) -> None:
        """
        Переміщає сутність на іншу сторону екрану, якщо він виходить за межі.
        """

        screen_width = self.level.settings["screen"]["width"]
        screen_height = self.level.settings["screen"]["height"]

        if self.rect.left > screen_width - 10:
            self.rect.right = 10
        elif self.rect.right < 10:
            self.rect.left = screen_width - 10

        if self.rect.top > screen_height - 10:
            self.rect.bottom = 10
        elif self.rect.bottom < 10:
            self.rect.top = screen_height - 10
