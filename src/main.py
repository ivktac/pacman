from engine.game import Game
from engine.settings import TomlSettings


def main() -> None:
    settings = TomlSettings()
    game = Game(settings)
    game.run()


if __name__ == "__main__":
    main()
