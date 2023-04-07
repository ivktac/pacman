import random

import pygame


from entities.entity import Entity, MovableEntity


class Ghost(MovableEntity):
    def __init__(
        self,
        x: int,
        y: int,
        speed: int,
        *groups,
    ) -> None:
        super().__init__(
            x * 40, y * 40, 32, speed, "assets/images/ghost.png", "ghost", *groups
        )

    def move(self, group: pygame.sprite.Group) -> None:
        if random.random() < 0.01:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.change_direction(dx, dy)

        if not hasattr(group, "player"):
            return

        player = group.player

        if self.is_player_is_sight(player):
            dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y

            if abs(dx) > abs(dy):
                self.change_direction(1 if dx > 0 else -1, 0)
            else:
                self.change_direction(0, 1 if dy > 0 else -1)

        super().move(group)

    def is_player_is_sight(self, entity: Entity) -> None:
        sight_distance = 200
        sight_rect = self.rect.inflate(sight_distance, sight_distance)

        if self.direction.x > 0:
            sight_rect.x += self.rect.width
        elif self.direction.x < 0:
            sight_rect.x -= sight_distance

        if self.direction.y > 0:
            sight_rect.y += self.rect.height
        elif self.direction.y < 0:
            sight_rect.y -= sight_distance

        return sight_rect.colliderect(entity.rect)
