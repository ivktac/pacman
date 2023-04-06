import sys
from functools import partial

import pygame

from entities import Pacman
from levels import Level
from settings import Settings


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            [self.settings.screen["width"], self.settings.screen["height"]]
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", self.settings.font["size"])

        self.score = 0

        self.level = Level(self)
        self.pacman = Pacman(self.level)
        self.control_mapping = self.create_control_mapping()

        self.load_level()

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
                    self.process_keydown_event(event.key)

    def process_keydown_event(self, key: int) -> None:
        action = self.control_mapping.get(key)
        if action is not None:
            action()

    def create_control_mapping(self) -> dict[int, callable]:
        """
        Створює словник, що містить відповідність між клавішами та діями.
        """

        controls = self.settings.controls
        control_mapping = {
            pygame.key.key_code(controls[direction]): partial(
                self.pacman.change_direction, dx, dy
            )
            for direction, (dx, dy) in {
                "up": (0, -1),
                "down": (0, 1),
                "left": (-1, 0),
                "right": (1, 0),
            }.items()
        }
        control_mapping[pygame.key.key_code(controls["pause"])] = self.pause_game

        return control_mapping

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
        self.display_score()
        pygame.display.flip()

    def clear_screen(self) -> None:
        """
        Очищує екран коліром, визначеним в налаштуваннях перед кожним кадром.
        """

        self.screen.fill(self.settings.colors["background"])

    def display_score(self) -> None:
        """
        Відображає поточний рахунок гравця.
        """

        score_text = self.font.render(
            f"Score: {self.score}", True, self.settings.colors["text"]
        )
        self.screen.blit(score_text, score_text.get_rect().move(10, 10))

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
