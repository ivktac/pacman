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

        self.image_idle = pygame.image.load(
            "assets/images/pacman.png").convert_alpha()
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.rect.topleft = (32, 32)

        walk_image = pygame.image.load(
            "assets/images/pacman_walk.png").convert_alpha()
        self.walk_frames = self.split_walk_frames(
            walk_image, frame_width=32, frame_height=32, num_frames=3)

        self.speed = self.level.settings.pacman["speed"]
        self.direction = pygame.math.Vector2(0, 0)

        self.frame_counter = 0
        self.current_frame = 0

    def split_walk_frames(self, image: pygame.Surface,
                          frame_width: int,
                          frame_height: int,
                          num_frames: int) -> list[pygame.Surface]:
        """
            Розділяє спрайт зі зображенням ходьби на окремі кадри.
        """

        frames = []
        for i in range(num_frames):
            frame = image.subsurface(
                (i * frame_width, 0, frame_width, frame_height))
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
                self.current_frame = (
                    self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]

        self.image = self.rotate()

    def move(self) -> None:
        """
            Оновлює положення Pacman.
        """

        new_position = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_position):
            self.rect = new_position

    def rotate(self) -> None:
        angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        return pygame.transform.rotate(self.image, angle)

    def check_collision(self, rect) -> bool:
        """
            Перевіряє чи не виникла колізія з іншими об’єктами.
        """

        for wall in self.level.walls:
            if wall.rect.colliderect(rect):
                return True
        return False

    def change_direction(self, x, y):
        """
            Змінює напрямок руху Pacman.
        """

        self.direction = pygame.math.Vector2(x, y)

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
    def __init__(self, level, x, y, width, height) -> None:
        super().__init__(level)

        self.color = self.level.settings.colors["wall"]

        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

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