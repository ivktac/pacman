import pygame
from engine.animation import Animation

from entities.entity import MovableEntity, Entity


class Player(MovableEntity):
    def __init__(self, x: int, y: int, *groups) -> None:
        super().__init__(x, y, 32, 3, "assets/images/pacman.png", "player", *groups)

        self.__image_idle = self.image

        self.__animation = Animation(
            {
                "walk": {"image_path": "assets/images/walk.png", "num_frames": 3},
                "explosion": {
                    "image_path": "assets/images/explosion.png",
                    "num_frames": 10,
                },
            },
            (self.size, self.size),
        )

        self.rect = self.image.get_rect()

        self.__score = 0

        self.__is_dead = False
        self.__death_time = 0

        self.__max_health = 3
        self.__health = self.__max_health

        self.__immunity_duration = 3000
        self.__immunity_end_time = 0

        self.__immunity = False

        self.__blink_duration = 200
        self.__blink_end_time = 0
        self.__visible = True

    def score(self) -> int:
        return self.__score

    def health(self) -> int:
        return self.__health

    def dead(self) -> bool:
        return self.__is_dead

    def time_since_death(self) -> int:
        return pygame.time.get_ticks() - self.__death_time

    def draw(self, screen: pygame.Surface) -> None:
        if self.__visible:
            screen.blit(self.image, self.rect.topleft)

    def update(self, group: pygame.sprite.Group) -> None:
        if self.__is_dead:
            return self.animate_explosion()

        if self.__health <= 0:
            return self.die()

        self.move(group)
        self.animate()

    def animate(self) -> None:
        if self.direction.magnitude() == 0:
            self.image = self.__image_idle
        else:
            self.update_pacman_frame()

        self.image = self.rotate()

        self.blink()

    def update_pacman_frame(self):
        self.__animation.update_frame("walk", 10)
        self.image = self.__animation.get_current_frame("walk")

    def rotate(self) -> pygame.Surface:
        angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        return pygame.transform.rotate(self.image, angle)

    def blink(self) -> None:
        self.check_immunity()

        if self.__immunity:
            if pygame.time.get_ticks() > self.__blink_end_time:
                self.__visible = not self.__visible
                self.__blink_end_time = pygame.time.get_ticks() + self.__blink_duration
        else:
            self.__visible = True

    def animate_explosion(self) -> None:
        current_time = pygame.time.get_ticks()

        elapsed_time = current_time - self.__death_time
        frame_delay = 3000 // len(self.__animation.animations["explosion"])

        self.__animation.current_frames["explosion"] = elapsed_time // frame_delay

        self.__animation.current_frames["explosion"] = min(
            self.__animation.current_frames["explosion"],
            len(self.__animation.animations["explosion"]) - 1,
        )

        self.image = self.__animation.get_current_frame("explosion")

        self.kill()

    def die(self) -> None:
        self.__is_dead = True
        self.__exploding = True
        self.__death_time = pygame.time.get_ticks()

        self.change_direction(0, 0)

    def eat_food(self, food: Entity) -> None:
        match str(food):
            case "cherry":
                self.increase_health()
            case "blueberry":
                self.give_immunity()
            case _:
                ...

        self.__score += food.points

    def respawn(self, x: int, y: int) -> None:
        dump_score = self.__score

        self.__init__(x, y)

        self.__score = dump_score

        self.rect.topleft = (x, y)

    def increase_health(self) -> None:
        self.__health = min(self.__health + 1, self.__max_health)

    def give_immunity(self) -> None:
        self.__immunity = True
        self.__immunity_end_time = pygame.time.get_ticks() + self.__immunity_duration

    def take_damage(self) -> None:
        if not self.__immunity:
            self.__health -= 1
            self.give_immunity()

    def check_collision(self, rect: pygame.Rect, group: pygame.sprite.Group) -> bool:
        for entity in group.sprites():
            if self.rect.colliderect(entity.rect):
                match str(entity):
                    case "ghost":
                        self.take_damage()
                    case "food" | "cherry" | "blueberry":
                        self.eat_food(entity)
                        entity.kill()

        return super().check_collision(rect, group)

    def check_immunity(self) -> None:
        if self.__immunity and pygame.time.get_ticks() > self.__immunity_end_time:
            self.__immunity = False

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
