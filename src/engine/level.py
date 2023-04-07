from typing import TYPE_CHECKING

import pygame

from entities.food import Food
from entities.wall import Wall
from entities.ghost import Ghost

if TYPE_CHECKING:
    from game import Game


class Level:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.settings = game.settings

        self.walls = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

    def clean(self) -> None:
        self.walls.empty()
        self.foods.empty()
        self.ghosts.empty()

    def create(self, data) -> None:
        self.clean()

        for y, line in enumerate(data):
            for x, tile in enumerate(line):
                match tile:
                    case "=":
                        self.walls.add(Wall(self, x, y))
                    case "P":
                        self.game.pacman.set_position(x * 40 + 5, y * 40 + 5)
                    case "*":
                        self.foods.add(Food(self, x, y))
                    case "C":
                        self.foods.add(Food(self, x, y, "cherry"))
                    case "S":
                        self.foods.add(Food(self, x, y, "blueberry"))
                    case "G":
                        self.ghosts.add(Ghost(self, x, y))

    def draw(self, screen: pygame.Surface) -> None:
        self.walls.draw(screen)
        self.foods.draw(screen)
        self.ghosts.draw(screen)
        self.game.pacman.draw(screen)

    def update(self) -> None:
        self.game.pacman.update()
        self.ghosts.update()

    def restart(self) -> None:
        self.clean()
        self.game.pacman.respawn()

    def is_completed(self) -> bool:
        return len(self.foods) == 0
