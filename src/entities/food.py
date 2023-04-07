import random
from entities.entity import Entity


class Food(Entity):
    def __init__(self, x: int, y: int, tag: str = "food", *groups) -> None:
        self.points = random.randint(1, 10)

        image_path = None

        match tag:
            case "cherry":
                image_path = "assets/images/cherry.png"
                tag = "cherry"
                self.points = 100
            case "blueberry":
                image_path = "assets/images/blueberry.png"
                tag = "blueberry"
                self.points = 300
            case _:
                tag = "food"

        if image_path is not None:
            entity = Entity.from_image(x * 40, y * 40, 32, image_path, tag, *groups)
        else:
            entity = Entity.from_color(
                x * 40 + 16, y * 40 + 16, 16, "yellow", tag, *groups
            )

        self.__dict__.update(entity.__dict__)
