from entities.entity import Entity


class Wall(Entity):
    def __init__(self, x: int, y: int, *groups) -> None:
        entity = Entity.from_image(
            x * 40, y * 40, 40, "assets/images/wall.png", "wall", *groups
        )

        self.__dict__.update(entity.__dict__)
