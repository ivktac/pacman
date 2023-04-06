from typing import TYPE_CHECKING
from entities.entity import Entity

if TYPE_CHECKING:
    from engine.level import Level


class Wall(Entity):
    def __init__(self, level: "Level", x: int, y: int) -> None:
        entity = Entity.from_image(level, size=40, image_path="assets/images/wall.png")

        self.__dict__.update(entity.__dict__)
        self.rect = self.image.get_rect(topleft=[x * self.size, y * self.size])
