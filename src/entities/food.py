import random
from typing import TYPE_CHECKING
from entities.entity import Entity

if TYPE_CHECKING:
    from engine.level import Level


class Food(Entity):
    def __init__(self, level: "Level", x: int, y: int, type: str | None = None) -> None:
        self.type = type
        self.points = random.randint(1, 10)

        image_path = None

        match self.type:
            case "cherry":
                image_path = "assets/images/cherry.png"
                self.points = 100
            case "blueberry":
                image_path = "assets/images/blueberry.png"
                self.points = 300
            case _:
                ...

        if image_path is not None:
            entity = Entity.from_image(level, size=36, image_path=image_path)
            position = [x * 40, y * 40]
        else:
            entity = Entity.from_color(level, size=16, color="yellow", shape="circle")
            position = [x * 40 + entity.size, y * 40 + entity.size]

        self.__dict__.update(entity.__dict__)
        self.rect = self.image.get_rect(topleft=position)
