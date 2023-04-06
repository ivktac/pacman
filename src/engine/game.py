import os
import sys
import pygame

from entities.pacman import Pacman
from engine.level import Level
from engine.settings import ISettings
from engine.menu import EndMenu, Menu, StartMenu, PauseMenu
from engine.ui import UI


class Game:
    def __init__(self, settings: ISettings) -> None:
        pygame.init()

        pygame.display.set_caption(settings["game"]["title"])  # type: ignore

        self.settings = settings
        self.screen = pygame.display.set_mode(
            (
                self.settings["screen"]["width"],
                self.settings["screen"]["height"],
            )  # type: ignore
        )

        self.clock = pygame.time.Clock()
        self.fps = self.settings["game"]["fps"]  # type: ignore

        self.font = pygame.font.SysFont(
            "Arial", self.settings["font"]["size"]
        )  # type: ignore
        self.ui = UI(self.font, self.settings)

        self.score = 0

        self.level = Level(self)
        self.current_level = 1

        self.pacman = Pacman(self.level)

        self.start_menu = StartMenu(self)
        self.paused_menu = PauseMenu(self)
        self.end_menu = EndMenu(self)
        self.current_menu: Menu | None = self.start_menu

        self.is_paused = False
        self.is_running = True

        self.is_debug = self.settings["game"]["debug"]  # type: ignore

    def run(self) -> None:
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.KEYDOWN:
                    if self.is_debug:
                        self.debug_handle_keydown(event.key)
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    if self.current_menu:
                        self.current_menu.handle_keydown(event.key)
                    else:
                        self.pacman.handle_keydown(event.key)

    def update(self) -> None:
        if self.current_menu:
            self.current_menu.update()
        else:
            if self.pacman.is_dead:
                self.restart()
                self.pacman.respawn()
                self.current_menu = self.end_menu
                return

            if self.level.is_completed():
                self.current_level += 1
                self.load_level()
                return

            self.level.update()

    def draw(self) -> None:
        self.clear_screen()

        if self.current_menu:
            self.current_menu.draw(self.screen)
        else:
            self.level.draw(self.screen)
            self.display_ui()

        pygame.display.flip()

    def clear_screen(self) -> None:
        self.screen.fill(self.settings["colors"]["background"])  # type: ignore

    def start(self) -> None:
        self.current_menu = None
        self.load_level()

    def pause(self) -> None:
        self.is_paused = True
        self.current_menu = self.paused_menu

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def resume(self) -> None:
        self.is_paused = False
        self.current_menu = None

    def restart(self) -> None:
        self.score = 0
        self.current_level = 1

        self.current_menu = None
        self.is_paused = False

        self.level.restart()
        self.load_level()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def display_ui(self) -> None:
        self.ui.display_score(self.screen, self.score)
        self.ui.display_level(self.screen, self.current_level)
        self.ui.display_health(self.screen, self.pacman.health)

    def load_level(self) -> None:
        filename = f"assets/levels/{self.current_level}.txt"
        if not os.path.exists(filename):
            self.current_menu = self.end_menu
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
                self.load_level()
