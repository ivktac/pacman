from game import Game
from settings import Settings


def main() -> None:
    settings = Settings()
    game = Game(settings)
    game.run()


if __name__ == '__main__':
    main()
