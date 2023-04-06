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
        pygame.display.set_caption(settings["game"]["title"])

        self.settings = settings
        self.screen = pygame.display.set_mode(
            [self.settings["screen"]["width"], self.settings["screen"]["height"]]
        )

        self.clock = pygame.time.Clock()
        self.fps = self.settings["game"]["fps"]

        self.font = pygame.font.SysFont("Arial", self.settings["font"]["size"])
        self.ui = UI(self.font, self.settings)

        self.score = 0

        self.level = Level(self)
        self.current_level = 1

        self.pacman = Pacman(self.level)

        self.start_menu = StartMenu(self)
        self.paused_menu = PauseMenu(self)
        self.end_menu = EndMenu(self)
        self.current_menu: Menu = self.start_menu

        self.is_paused = False
        self.is_running = True

        self.is_debug = self.settings["game"]["debug"]

    def run(self) -> None:
        """
        Запускає гру.
        """

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

    def handle_events(self) -> None:
        """
        Обробляє події, такі як натискання клавіш і закриття вікна.
        """

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
        """
        Оновлює стан гри, викликавши метод оновлення об’єкта Level.

        Цей метод відповідає за оновлення позицій і станів усіх ігрових об’єктів.
        """

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
        """
        Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.

        Цей метод відповідає за відтворення всіх ігрових об’єктів на екрані.
        """

        self.clear_screen()

        if self.current_menu:
            self.current_menu.draw(self.screen)
        else:
            self.level.draw(self.screen)
            self.display_ui()

        pygame.display.flip()

    def clear_screen(self) -> None:
        """
        Очищує екран коліром, визначеним в налаштуваннях перед кожним кадром.
        """

        self.screen.fill(self.settings["colors"]["background"])

    def start(self) -> None:
        self.current_menu = None
        self.load_level()

    def pause(self) -> None:
        """
        Зупиняє гру та показує меню з такими опціями:
            - `Продовжити` - продовжує гру
            - `Перезапустити` - починає гру з початку
            - `Вийти` - виходить з гри
        """

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
        """
        Перезапускає гру.
        """

        self.current_menu = None
        self.is_paused = False
        self.level.restart()
        self.score = 0
        self.current_level = 1
        self.load_level()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def display_ui(self) -> None:
        """
        Відображає інтерфейс користувача, такий як:
            - рахунок
            - рівень
            - життя
        """

        self.ui.display_score(self.screen, self.score)
        self.ui.display_level(self.screen, self.current_level)
        self.ui.display_health(self.screen, self.pacman.health)

    def load_level(self) -> None:
        """
        Завантажує дані рівня та створює відповідні об’єкти.
        """

        try:
            self.level.load(self.current_level)
        except FileNotFoundError:
            self.current_menu = self.end_menu

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