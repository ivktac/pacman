import sys
from functools import partial

import pygame

from entities.pacman import Pacman
from level import Level
from settings import ISettings

from menu import StartMenu, PauseMenu
from ui import UI


class Game:
    def __init__(self, settings: ISettings) -> None:
        pygame.init()
        pygame.display.set_caption(settings["screen"]["title"])

        self.settings = settings
        self.screen = pygame.display.set_mode(
            [self.settings["screen"]["width"], self.settings["screen"]["height"]]
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", self.settings["font"]["size"])
        self.ui = UI(self.font, self.settings)

        self.score = 0

        self.level = Level(self)
        self.current_level = 1

        self.pacman = Pacman(self.level)

        self.start_menu = StartMenu(self)
        self.paused_menu = PauseMenu(self)
        self.current_menu = self.start_menu
        self.is_paused = False


    def run(self) -> None:
        """
        Запускає гру.
        """

        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings["screen"]["fps"])

    def handle_events(self) -> None:
        """
        Обробляє події, такі як натискання клавіш і закриття вікна.
        """

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    if self.current_menu:
                        self.current_menu.handle_keydown(event.key)
                    elif self.is_paused:
                        self.paused_menu.handle_keydown(event.key)
                    else:
                        self.pacman.handle_keydown(event.key)

    def update(self) -> None:
        """
        Оновлює стан гри, викликавши метод оновлення об’єкта Level.

        Цей метод відповідає за оновлення позицій і станів усіх ігрових об’єктів.
        """

        if self.current_menu:
            self.start_menu.update()
        elif self.is_paused:
            self.paused_menu.update()
        else:
            if self.pacman.is_dead:
                self.restart()
                self.pacman.respawn()
                return

            if self.level.is_completed():
                self.current_level += 1
                self.load_level()
                self.pacman.direction = pygame.math.Vector2(0, 0)
                return

            self.level.update()

    def draw(self) -> None:
        """
        Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.

        Цей метод відповідає за відтворення всіх ігрових об’єктів на екрані.
        """

        self.clear_screen()

        if self.current_menu:
            self.start_menu.draw(self.screen)
        elif self.is_paused:
            self.paused_menu.draw(self.screen)
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

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def resume(self) -> None:
        self.is_paused = False

    def restart(self) -> None:
        """
        Перезапускає гру.
        """

        self.is_paused = False
        self.level.restart()
        self.pacman.direction = pygame.math.Vector2(0, 0)
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

    def show_menu(self) -> None:
        """
        Відображає меню гри з такими опціями:
            - `Нова гра` - починає гру з початку
            - `Вийти` - виходить з гри
        """
        pass

    def load_level(self) -> None:
        """
        Завантажує дані рівня та створює відповідні об’єкти.
        """

        self.level.load(self.current_level)
