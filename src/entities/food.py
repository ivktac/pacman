import random
from typing import TYPE_CHECKING
from entities.entity import Entity

if TYPE_CHECKING:
    from engine.level import Level


class Food(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        size = level.settings["food"]["size"]
        color = level.settings["colors"]["food"]

        super().__init__(level, size=size, color=color)

        wall_size = level.settings["wall"]["size"]
        self.rect = self.image.get_rect(
            topleft=[x * wall_size + self.size, y * wall_size + self.size]
        )

        self.points = random.randint(1, 10)
