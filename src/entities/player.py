import pygame
from pacman.settings import HEIGHT, MAX_HEALTH, WIDTH, PLAYER_SPEED, IMMUNITY_TIME


class Player(pygame.sprite.Sprite):
    rect: pygame.rect.Rect

    def __init__(self, position, obstacle_sprites, *groups) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(
            "assets/images/player.png").convert_alpha()

        self.start_position = position
        self.rect = self.image.get_rect(topleft=position)
        self.enemies = [enemy for enemy in obstacle_sprites
                        if hasattr(enemy, "enemy_update")]

        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = PLAYER_SPEED
        self.health = self.max_health = MAX_HEALTH

        self.immune = False
        self.start_time_immunity = 0
        self.time_immune = self.start_time_immunity + IMMUNITY_TIME

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self) -> None:
        self.input()
        self.move()
        self.update_immunity()

    def move(self) -> None:
        self.normalize_direction()

        self.rect.x += int(self.direction.x * self.speed)
        self.collide(self.direction.x, 0, walls=self.obstacle_sprites)
        self.rect.y += int(self.direction.y * self.speed)
        self.collide(0, self.direction.y, walls=self.obstacle_sprites)

        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.top = HEIGHT

        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = WIDTH

    def normalize_direction(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def collide(self, xvel, yvel, walls) -> None:
        for wall in walls:
            if self.rect.colliderect(wall.hitbox):
                self.swap_position(xvel, yvel, self.rect, wall)

    def swap_position(self, xvel, yvel, rect, wall):
        if xvel > 0:
            rect.right = wall.hitbox.left
        if xvel < 0:
            rect.left = wall.hitbox.right
        if yvel > 0:
            rect.bottom = wall.hitbox.top
        if yvel < 0:
            rect.top = wall.hitbox.bottom

    def collide_enemy(self, enemy) -> None:
        if self.immune:
            return

        if self.rect.colliderect(enemy.rect):
            self.health -= enemy.damage
            self.immune = True
            self.speed = PLAYER_SPEED + 2
            self.start_time_immunity = pygame.time.get_ticks()
            self.time_immune = self.start_time_immunity + IMMUNITY_TIME

    def update_immunity(self) -> None:
        if self.immune:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

        if self.time_immune <= pygame.time.get_ticks():
            self.immune = False
            self.speed = 5