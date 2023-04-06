import sys
import pygame
from settings import Settings
from entities import Pacman
from levels import Level


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            [self.settings.screen["width"], self.settings.screen["height"]])
        self.clock = pygame.time.Clock()

        self.level = Level(self)
        self.load_level()
        self.pacman = Pacman(self.level)

    def run(self) -> None:
        """
            Запускає гру.
        """

        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.screen["fps"])

    def handle_events(self) -> None:
        """
            Обробляє події, такі як натискання клавіш і закриття вікна.
        """

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.pause_game()
                        case pygame.K_UP:
                            self.pacman.change_direction(0, -1)
                        case pygame.K_DOWN:
                            self.pacman.change_direction(0, 1)
                        case pygame.K_LEFT:
                            self.pacman.change_direction(-1, 0)
                        case pygame.K_RIGHT:
                            self.pacman.change_direction(1, 0)

    def update(self) -> None:
        """
            Оновлює стан гри, викликавши метод оновлення об’єкта Level.

            Цей метод відповідає за оновлення позицій і станів усіх ігрових об’єктів.
        """

        self.level.update()

    def draw(self) -> None:
        """
            Малює елементи гри на екрані, викликавши метод малювання об’єкта Level.

            Цей метод відповідає за відтворення всіх ігрових об’єктів на екрані.
        """

        self.clear_screen()
        self.level.draw(self.screen)
        pygame.display.flip()

    def clear_screen(self) -> None:
        """
            Очищує екран коліром, визначеним в налаштуваннях перед кожним кадром.
        """

        self.screen.fill(self.settings.colors["background"])

    def show_menu(self) -> None:
        """
            Відображає меню гри з такими опціями:
                - `Нова гра` - починає гру з початку
                - `Налаштування` - відкриває меню налаштувань
                - `Вийти` - виходить з гри
        """
        pass

    def pause_game(self) -> None:
        """ 
            Зупиняє гру та показує меню з такими опціями:
                - `Продовжити` - продовжує гру
                - `Перезапустити` - починає гру з початку
                - `Вийти` - виходить з гри
        """
        pass

    def load_level(self, level_number=None) -> None:
        """
            Завантажує дані рівня та створює відповідні об’єкти.
        """

        if level_number is None:
            level_number = self.level.current_level
        self.level.load_level(level_number)
