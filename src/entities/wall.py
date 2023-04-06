from typing import TYPE_CHECKING
from entities.entity import Entity

if TYPE_CHECKING:
    from engine.level import Level


class Wall(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        super().__init__(level, size=40, image_path="assets/images/wall.png")

        self.rect = self.image.get_rect(topleft=[x * self.size, y * self.size])
