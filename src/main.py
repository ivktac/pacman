import pygame

from engine.game import Game

FPS = 60
SCREEN_SIZE = (800, 800)


def main() -> None:
    pygame.init()

    pygame.display.set_caption("Pacman")

    screen = pygame.display.set_mode(SCREEN_SIZE)

    clock = pygame.time.Clock()

    game = Game()

    while game:
        game.handle_events()
        game.update()
        game.draw(screen)

        clock.tick(60)


if __name__ == "__main__":
    main()
