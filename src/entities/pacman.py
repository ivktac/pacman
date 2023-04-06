import pygame

from typing import TYPE_CHECKING

from entities.entity import MovableEntity
from entities.food import Food

if TYPE_CHECKING:
    from engine.level import Level


class Pacman(MovableEntity):
    def __init__(self, level: "Level") -> None:
        size = level.settings["pacman"]["size"]
        speed = level.settings["pacman"]["speed"]
        image_path = level.settings["pacman"]["image"]
        walk_path = level.settings["pacman"]["walk"]

        super().__init__(level, size=size, speed=speed, image_path=image_path)

        self.image_idle = pygame.image.load(image_path).convert_alpha()

        walk_image = pygame.image.load(walk_path).convert_alpha()
        self.walk_frames = self.split_walk_frames(walk_image, [self.size, self.size], 3)

        self.image = self.image_idle
        self.rect = self.image.get_rect()

        self.frame_counter = 0
        self.current_frame = 0

        self.is_dead = False

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
        self.eat_food()

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

    def rotate(self) -> None:
        angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        return pygame.transform.rotate(self.image, angle)


    def die(self) -> None:
        """
        Переводить Pacman в стан смерті.
        """

        self.is_dead = True

    def check_collision(self, rect: pygame.Rect) -> None:
        """
        Перевіряє чи не зіткнувся Pacman з іншими об’єктами.
        """

        collided_ghosts = pygame.sprite.spritecollide(self, self.level.ghosts, False)
        if collided_ghosts:
            self.die()

        return super().check_collision(rect)

    def change_direction(self, x: int, y: int):
        """
        Змінює напрямок руху Pacman.
        """

        self.direction = pygame.math.Vector2(x, y)

    def set_position(self, x: int, y: int):
        """
        Задає положення Pacman.
        """

        self.rect.topleft = [x, y]

    def eat_food(self):
        """
        Перевіряє чи не з’їв Pacman їжу.
        """
        collided_food = pygame.sprite.spritecollide(self, self.level.foods, True)
        for food in collided_food:
            self.food_eaten(food)

    def food_eaten(self, food: Food) -> None:
        """
        Збільшує кількість зібраної Pacman їжі.
        """

        self.level.game.score += food.points

    def respawn(self) -> None:
        """
        Скидає стан Pacman до початкового.
        """

        self.is_dead = False
        self.reset()

    def reset(self) -> None:
        """
        Скидає стан Pacman до початкового.
        """

        self.image = self.image_idle
        self.direction = pygame.math.Vector2(0, 0)

    def handle_keydown(self, key: int) -> None:
        """
        Обробляє натискання клавіш.
        """

        match key:
            case pygame.K_UP | pygame.K_w:
                self.change_direction(0, -1)
            case pygame.K_DOWN | pygame.K_s:
                self.change_direction(0, 1)
            case pygame.K_LEFT | pygame.K_a:
                self.change_direction(-1, 0)
            case pygame.K_RIGHT | pygame.K_d:
                self.change_direction(1, 0)