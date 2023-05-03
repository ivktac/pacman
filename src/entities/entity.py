import pygame


class Entity(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, x: int, y: int, size: int, tag: str, *groups) -> None:
        super().__init__(*groups)

        self.__x = x
        self.__y = y
        self.__size = size
        self.__tag = tag

    @property
    def size(self) -> int:
        return self.__size

    @classmethod
    def from_image(cls, x: int, y: int, size: int, image_path: str, tag: str, *groups):
        entity = cls(x, y, size, tag, *groups)

        entity.image = pygame.image.load(image_path).convert_alpha()
        entity.image = pygame.transform.scale(
            entity.image, (entity.__size, entity.__size)
        )
        entity.rect = entity.image.get_rect(topleft=[entity.__x, entity.__y])

        return entity

    @classmethod
    def from_color(cls, x: int, y: int, size: int, color: str, tag: str, *groups):
        entity = cls(x, y, size, tag, *groups)
        entity.image = pygame.Surface(
            [entity.__size, entity.__size], pygame.SRCALPHA, 32
        ).convert_alpha()

        pygame.draw.circle(
            entity.image,
            color,
            (entity.__size // 2, entity.__size // 2),
            entity.__size // 2,
        )
        entity.rect = entity.image.get_rect(topleft=[entity.__x, entity.__y])

        return entity

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def __str__(self) -> str:
        return self.__tag

    def update(self, _: pygame.sprite.Group) -> None:
        ...


class MovableEntity(Entity):
    def __init__(
        self, x: int, y: int, size: int, speed: int, image_path: str, tag: str, *groups
    ) -> None:
        entity = Entity.from_image(x, y, size, image_path, tag, *groups)
        self.__dict__.update(entity.__dict__)

        self.__speed = speed
        self.__direction = pygame.math.Vector2(0, 0)

    @property
    def direction(self) -> pygame.math.Vector2:
        return self.__direction

    @property
    def speed(self) -> int:
        return self.__speed

    def update(self, group: pygame.sprite.Group) -> None:
        self.move(group)

    def move(self, group: pygame.sprite.Group) -> None:
        new_position = self.rect.move(self.__direction * self.__speed)

        if not self.check_collision(new_position, group):
            self.rect = new_position

        self.wrap_around()

    def check_collision(self, rect: pygame.Rect, group: pygame.sprite.Group) -> bool:
        for entity in group.sprites():
            if str(entity) == "wall":
                if rect.colliderect(entity.rect):
                    return True

        return False

    def wrap_around(self) -> None:
        gap = 10
        screen_width, screen_height = pygame.display.get_surface().get_size()

        if self.rect.left > screen_width - gap:
            self.rect.right = gap
        elif self.rect.right < gap:
            self.rect.left = screen_width - gap

        if self.rect.top > screen_height - gap:
            self.rect.bottom = gap
        elif self.rect.bottom < gap:
            self.rect.top = screen_height - gap

    def change_direction(self, x: int, y: int):
        self.__direction = pygame.math.Vector2(x, y)
