from engine.game import Game
from engine.settings import JsonSettings


def main() -> None:
    settings = JsonSettings()
    game = Game(settings)
    game.run()


if __name__ == "__main__":
    main()
