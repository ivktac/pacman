import pygame

from typing import TYPE_CHECKING
from entities.food import Food
from entities.entity import MovableEntity

if TYPE_CHECKING:
    from engine.level import Level


class Pacman(MovableEntity):
    def __init__(self, level: "Level") -> None:
        super().__init__(level, size=32, speed=3, image_path="assets/images/pacman.png")

        self.image_idle = pygame.image.load("assets/images/pacman.png").convert_alpha()

        walk_image = pygame.image.load("assets/images/walk.png").convert_alpha()
        self.walk_frames = self.split_walk_frames(walk_image, [self.size, self.size], 3)

        self.image = self.image_idle
        self.rect = self.image.get_rect()

        self.frame_counter = 0
        self.current_frame = 0

        self.is_dead = False

        self.max_health = 3
        self.health = self.max_health

        self.immunity_duration = 3000
        self.immunity_end_time = 0

        self.immunity = False

        self.blink_duration = 200
        self.blink_end_time = 0
        self.visible = True

    @staticmethod
    def split_walk_frames(
        image: pygame.Surface, frame_size: tuple[int, int], num_frames: int
    ) -> list[pygame.Surface]:
        frame_width, frame_height = frame_size

        frames = []
        for i in range(num_frames):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    def draw(self, screen: pygame.Surface) -> None:
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def update(self) -> None:
        if self.health <= 0:
            return self.die()

        self.move()
        self.animate()

    def animate(self) -> None:
        if self.direction.magnitude() == 0:
            self.image = self.image_idle
        else:
            self.update_pacman_frame()

        self.image = self.rotate()

        self.blink()

    def update_pacman_frame(self):
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        self.image = self.walk_frames[self.current_frame]

    def rotate(self) -> None:
        angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        return pygame.transform.rotate(self.image, angle)

    def blink(self) -> None:
        self.check_immunity()

        if self.immunity:
            if pygame.time.get_ticks() > self.blink_end_time:
                self.visible = not self.visible
                self.blink_end_time = pygame.time.get_ticks() + self.blink_duration
        else:
            self.visible = True

    def die(self) -> None:
        self.is_dead = True

    def eat_food(self, food: Food) -> None:
        match food.type:
            case "cherry":
                self.increase_health()
            case "blueberry":
                self.give_immunity()
            case _:
                ...

        self.level.game.score += food.points

    def respawn(self) -> None:
        self.__init__(self.level)

    def increase_health(self) -> None:
        self.health = min(self.health + 1, self.max_health)

    def give_immunity(self) -> None:
        self.immunity = True
        self.immunity_end_time = pygame.time.get_ticks() + self.immunity_duration

    def take_damage(self) -> None:
        if not self.immunity:
            self.health -= 1
            self.give_immunity()

    def check_collision(self, rect: pygame.Rect) -> None:
        collided_ghosts = pygame.sprite.spritecollide(self, self.level.ghosts, False)
        if collided_ghosts:
            self.take_damage()

        collided_food = pygame.sprite.spritecollide(self, self.level.foods, True)
        for food in collided_food:
            self.eat_food(food)

        return super().check_collision(rect)

    def check_immunity(self) -> None:
        if self.immunity and pygame.time.get_ticks() > self.immunity_end_time:
            self.immunity = False

    def change_direction(self, x: int, y: int):
        self.direction = pygame.math.Vector2(x, y)

    def set_position(self, x: int, y: int):
        self.rect.topleft = [x, y]
        self.direction = pygame.math.Vector2(0, 0)

    def handle_keydown(self, key: int) -> None:
        match key:
            case pygame.K_UP | pygame.K_w:
                self.change_direction(0, -1)
            case pygame.K_DOWN | pygame.K_s:
                self.change_direction(0, 1)
            case pygame.K_LEFT | pygame.K_a:
                self.change_direction(-1, 0)
            case pygame.K_RIGHT | pygame.K_d:
                self.change_direction(1, 0)
