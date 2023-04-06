from typing import TYPE_CHECKING
from entity import MovableEntity


if TYPE_CHECKING:
    from level import Level


class Ghost(MovableEntity):
    def __init__(self, level: "Level") -> None:
        size = level.settings.ghost["size"]
        speed = level.settings.ghost["speed"]
        image_path = level.settings.ghost["image"]

        super().__init__(level, size=size, speed=speed, image_path=image_path)

        self.rect = self.image.get_rect()