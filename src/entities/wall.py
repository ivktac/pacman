from typing import TYPE_CHECKING
from entities.entity import Entity

if TYPE_CHECKING:
    from level import Level


class Wall(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        size = level.settings["wall"]["size"]
        image_path = level.settings["wall"]["image"]

        super().__init__(level, size=size, image_path=image_path)

        self.rect = self.image.get_rect(topleft=[x * self.size, y * self.size])
