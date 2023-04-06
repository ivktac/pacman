import pygame

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from engine.level import Level


class Entity(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, level: "Level") -> None:
        super().__init__()

        self.level = level

    @classmethod
    def from_image(cls, level: "Level", size: int, image_path: str):
        entity = cls(level)

        entity.size = size
        entity.image = pygame.image.load(image_path).convert_alpha()
        entity.image = pygame.transform.scale(entity.image, (entity.size, entity.size))

        return entity

    @classmethod
    def from_color(cls, level: "Level", size: int, color: str, shape: str = "circle"):
        entity = cls(level)
        entity.size = size
        entity.image = pygame.Surface([size, size], pygame.SRCALPHA, 32).convert_alpha()

        match shape:
            case "circle":
                pygame.draw.circle(
                    entity.image, color, (size // 2, size // 2), size // 2
                )
            case "square":
                pygame.draw.rect(entity.image, color, (0, 0, size, size))

        return entity

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self) -> None:
        ...


class MovableEntity(Entity):
    def __init__(self, level: "Level", size: int, speed: int, image_path: str) -> None:
        entity = Entity.from_image(level, size, image_path)
        self.__dict__.update(entity.__dict__)

        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)

    def update(self) -> None:
        self.move()

    def move(self) -> None:
        new_position = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_position):
            self.rect = new_position

        self.wrap_around()

    def check_collision(self, rect: pygame.Rect) -> bool:
        for wall in self.level.walls:
            if wall.rect.colliderect(rect):
                return True

        return False

    def wrap_around(self) -> None:
        screen_width, screen_height = pygame.display.get_surface().get_size()

        if self.rect.left > screen_width - 10:
            self.rect.right = 10
        elif self.rect.right < 10:
            self.rect.left = screen_width - 10

        if self.rect.top > screen_height - 10:
            self.rect.bottom = 10
        elif self.rect.bottom < 10:
            self.rect.top = screen_height - 10
