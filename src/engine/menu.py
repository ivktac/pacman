from abc import ABC, abstractmethod
import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.game import Game


class IMenu(ABC):
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        ...


class Menu(IMenu):
    def __init__(
        self,
        options: list[tuple[str, callable]],
        font: pygame.font.Font,
        colors: dict[str, str],
    ) -> None:
        self.options = options
        self.font = font
        self.colors = colors
        self.current_option = 0

    def draw(self, screen: pygame.Surface) -> None:
        width, height = screen.get_size()
        option_height = height // (len(self.options) + 1)

        for i, (option_text, _) in enumerate(self.options):
            color = (
                self.colors["selected"]
                if i == self.current_option
                else self.colors["text"]
            )
            option_surface = self.font.render(option_text, True, color)
            option_rect = option_surface.get_rect()
            option_rect.center = width // 2, (i + 1) * option_height
            screen.blit(option_surface, option_rect)

    def handle_keydown(self, key: int) -> None:
        match key:
            case pygame.K_UP:
                self.next_option()
            case pygame.K_DOWN:
                self.previous_option()
            case pygame.K_RETURN:
                self.select_option()

    def next_option(self) -> None:
        self.current_option -= 1
        if self.current_option < 0:
            self.current_option = len(self.options) - 1

    def previous_option(self) -> None:
        self.current_option += 1
        if self.current_option >= len(self.options):
            self.current_option = 0

    def select_option(self) -> None:
        _, action = self.options[self.current_option]
        action()

    def update(self) -> None:
        ...


class StartMenu(Menu):
    def __init__(self, game: "Game") -> None:
        options = [
            ("Нова гра", game.start),
            ("Вийти", game.quit),
        ]
        super().__init__(options, game.font, game.settings["colors"])


class PauseMenu(Menu):
    def __init__(self, game: "Game") -> None:
        options = [
            ("Продовжити", game.resume),
            ("Нова гра", game.restart),
            ("Вийти", game.quit),
        ]
        super().__init__(options, game.font, game.settings["colors"])


class EndMenu(Menu):
    def __init__(self, game: "Game") -> None:
        options = [
            ("Перезапустити", game.restart),
            ("Вийти", game.quit),
        ]
        super().__init__(options, game.font, game.settings["colors"])

        self.game_end_text = "Гра завершена!"
        self.game_end_surface = self.font.render(
            self.game_end_text, True, game.settings["colors"]["end"]
        )
        self.game_end_rect = self.game_end_surface.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        width, height = screen.get_size()

        self.game_end_rect.center = width // 2, height // 4
        screen.blit(self.game_end_surface, self.game_end_rect)

        return super().draw(screen)
