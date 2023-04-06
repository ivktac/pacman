from engine.game import Game
from engine.settings import Settings


def main() -> None:
    settings = Settings()
    game = Game(settings)
    game.run()


if __name__ == '__main__':
    main()
