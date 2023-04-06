import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from levels import Level


class Entity(pygame.sprite.Sprite):
    def __init__(self, level: "Level") -> None:
        super().__init__()

        self.level = level
        # ... common entity properties


class Pacman(Entity):
    def __init__(self, level: "Level") -> None:
        super().__init__(level)

        self.size = self.level.settings.pacman["size"]
        image_path = self.level.settings.pacman["image"]
        self.image_idle = pygame.image.load(image_path).convert_alpha()

        walk_path = self.level.settings.pacman["walk"]
        walk_image = pygame.image.load(walk_path).convert_alpha()
        self.walk_frames = self.split_walk_frames(walk_image, [self.size, self.size], 3)

        self.image = self.image_idle
        self.rect = self.image.get_rect()

        self.speed = self.level.settings.pacman["speed"]
        self.direction = pygame.math.Vector2(0, 0)

        self.frame_counter = 0
        self.current_frame = 0

    def split_walk_frames(
        self, image: pygame.Surface, frame_size: tuple[int, int], num_frames: int
    ) -> list[pygame.Surface]:
        """
        Розділяє спрайт зі зображенням ходьби на окремі кадри.
        """

        frame_width, frame_height = frame_size

        frames = []
        for i in range(num_frames):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    def update(self) -> None:
        """
        Оновлює стан Pacman, як-от положення та взаємодію з іншими об’єктами.
        """

        self.move()
        self.animate()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Відображає Pacman на екрані.
        """

        screen.blit(self.image, self.rect)

    def animate(self) -> None:
        """
        Оновлює зображення Pacman, як-от зміну кадру анімації.
        """

        if self.direction.magnitude() == 0:
            self.image = self.image_idle
        else:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]

        self.image = self.rotate()

    def move(self) -> None:
        """
        Оновлює положення Pacman.
        """

        new_position = self.rect.move(self.direction * self.speed)        
        if not self.check_collision(new_position):
            self.rect = new_position

        self.wrap_around()

    def rotate(self) -> None:
        angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        return pygame.transform.rotate(self.image, angle)

    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Перевіряє чи не виникла колізія з іншими об’єктами.
        """

        for wall in self.level.walls:
            if rect.colliderect(wall.rect):
                return True
        return False

    def wrap_around(self) -> None:
        """
        Переміщає Pacman на іншу сторону екрану, якщо він виходить за межі.
        """

        screen_width = self.level.settings.screen["width"]
        screen_height = self.level.settings.screen["height"]

        if self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = screen_width
        
        if self.rect.top > screen_height:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = screen_height

    def change_direction(self, x, y):
        """
        Змінює напрямок руху Pacman.
        """

        self.direction = pygame.math.Vector2(x, y)

    def set_position(self, x, y):
        """
        Задає положення Pacman.
        """

        self.rect = self.rect.move(x, y)

    def increase_hearts(self, amount):
        """
        Збільшує кількість сердець Pacman на задану кількість.
        """
        pass

    def decrease_hearts(self, amount):
        """
        Зменшує кількість сердець Pacman на задану кількість.
        """
        pass


class Wall(Entity):
    def __init__(self, level, x, y) -> None:
        super().__init__(level)

        self.size = self.level.settings.wall["size"]
        self.color = self.level.settings.colors["wall"]

        image_path = self.level.settings.wall["image"]
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, [self.size, self.size])

        self.rect = self.image.get_rect(topleft=[x * self.size, y * self.size])

    def draw(self, screen):
        """
        Відображає стіну на екрані.
        """

        screen.blit(self.image, self.rect)


class Ghost(Entity):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Ghost properties


class Food(Entity):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Food properties


class Inky(Ghost):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Inky properties


class Clyde(Ghost):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Clyde properties


class Blinky(Ghost):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Blinky properties


class Pinky(Ghost):
    def __init__(self, level) -> None:
        super().__init__(level)
        # ... specific Pinky properties
