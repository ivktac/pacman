import os
import sys
import pygame
from engine.settings import TomlSettings

from entities.pacman import Pacman
from engine.level import Level
from engine.ui.menus import Menu
from engine.ui.ui import UI


class Game:
    def __init__(self) -> None:
        self.settings = TomlSettings()

        self.score = 0

        self.level = Level(self)
        self.current_level = 0

        self.pacman = Pacman(self.level)

        self.menu = Menu(
            {"start": self.start, "quit": self.quit, "resume": self.resume}
        )

        self.ui = UI()

        self.menu.open_main()

        self.is_paused = False
        self.__is_running = True

        self.is_debug = False

    def handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.KEYDOWN:
                    if self.is_debug:
                        self.debug_handle_keydown(event.key)
                    self.menu.handle_keydown(event.key)
                    self.pacman.handle_keydown(event.key)

    def update(self) -> None:
        self.menu.update()

        if (
            self.pacman.is_dead
            and pygame.time.get_ticks() - self.pacman.death_time > 3500
        ):
            self.menu.open_new_record()
            return

        if self.level.is_completed():
            self.current_level += 1
            self.load_level()
            return

        self.level.update()

    def draw(self, screen: pygame.Surface) -> None:
        self.clear_screen(screen)

        if self.menu.is_open():
            self.menu.draw(screen)
        else:
            self.level.draw(screen)
            self.ui.display(
                screen,
                pygame.font.SysFont("Arial", self.menu.get_current_font_size()),
                self.score,
                self.current_level,
                self.pacman.health,
            )

        pygame.display.flip()

    def clear_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")  # type: ignore

    def start(self) -> None:
        self.menu.close()
        self.load_level()

    def pause(self) -> None:
        self.is_paused = True
        self.menu.open_pause()

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def resume(self) -> None:
        self.is_paused = False
        self.menu.close()

    def restart(self) -> None:
        self.score = 0
        self.current_level = 1

        self.menu.close()

        self.is_paused = False

        self.level.restart()
        self.load_level()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def resize_screen(self, width: int, height: int) -> None:
        pygame.display.set_mode((width, height))

    def resize_font(self, size: int) -> None:
        self.font = pygame.font.SysFont("Arial", size)
        self.ui = UI(self.font, self.settings)

    def load_level(self) -> None:
        filename = f"assets/levels/{self.current_level}.txt"
        if not os.path.exists(filename):
            self.menu.open_game_over()
            return

        with open(filename, "r") as file:
            self.level.create(file.readlines())

    def debug_handle_keydown(self, key: int) -> None:
        match key:
            case pygame.K_F1:
                self.restart()
            case pygame.K_F2:
                self.current_level += 1
                self.load_level()
            case pygame.K_F3:
                self.current_level -= 1
                if self.current_level < 1:
                    self.current_level = 1
                self.load_level()
            case pygame.K_F4:
                self.pacman.die()

    def __bool__(self) -> bool:
        return self.__is_running
