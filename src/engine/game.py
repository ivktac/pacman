import os
import sys
import pygame

from entities.pacman import Pacman
from engine.level import Level
from engine.settings import ISettings
from engine.ui.menu_loader import MenuLoader

from engine.ui.ui import UI


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
        self.current_level = 0

        self.pacman = Pacman(self.level)

        self.menu_loader = MenuLoader(self)
        self.menu_loader.show_menu("start")

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
                    self.menu_loader.handle_keydown(event.key)
                    self.pacman.handle_keydown(event.key)

    def update(self) -> None:
        self.menu_loader.update()

        if (
            self.pacman.is_dead
            and pygame.time.get_ticks() - self.pacman.death_time > 3500
        ):
            self.menu_loader.show_menu("game_over")
            return

        if self.level.is_completed():
            self.current_level += 1
            self.load_level()
            return

        self.level.update()

    def draw(self) -> None:
        self.clear_screen()

        if len(self.menu_loader) > 0:
            self.menu_loader.draw(self.screen)
        else:
            self.level.draw(self.screen)
            self.display_ui()

        pygame.display.flip()

    def clear_screen(self) -> None:
        self.screen.fill(self.settings["colors"]["background"])  # type: ignore

    def start(self) -> None:
        self.menu_loader.clear()
        self.load_level()

    def pause(self) -> None:
        self.is_paused = True
        self.menu_loader.show_menu("pause")

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def resume(self) -> None:
        self.is_paused = False
        self.menu_loader.clear()

    def restart(self) -> None:
        self.score = 0
        self.current_level = 1

        self.menu_loader.clear()

        self.is_paused = False

        self.level.restart()
        self.load_level()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def show_settings_menu(self) -> None:
        self.menu_loader.show_menu("settings")

    def show_previous_menu(self) -> None:
        self.menu_loader.show_previous_menu()

    def display_ui(self) -> None:
        self.ui.display_score(self.screen, self.score)
        self.ui.display_level(self.screen, self.current_level)
        self.ui.display_health(self.screen, self.pacman.health)

    def resize_screen(self, width: int, height: int) -> None:
        self.screen = pygame.display.set_mode((width, height))

    def resize_font(self, size: int) -> None:
        self.font = pygame.font.SysFont("Arial", size)
        self.ui = UI(self.font, self.settings)

    def load_level(self) -> None:
        filename = f"assets/levels/{self.current_level}.txt"
        if not os.path.exists(filename):
            self.menu_loader.show_menu("win")
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
