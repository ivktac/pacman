import pygame

from engine.ui.menu import (
    Menu,
    StartMenu,
    PauseMenu,
    EndMenu,
    SettingsMenu,
    GameOverMenu,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.game import Game


class MenuLoader:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.menus = {
            "start": StartMenu(game),
            "pause": PauseMenu(game),
            "end": EndMenu(game),
            "settings": SettingsMenu(game),
            "game_over": GameOverMenu(game),
        }

        self.menu_stack: list[Menu] = []

    def show_menu(self, name: str) -> None:
        self.menu_stack.append(self.menus[name])

    def show_previous_menu(self) -> None:
        self.menu_stack.pop()

    def clear(self) -> None:
        self.menu_stack.clear()

    def update(self) -> None:
        if self.menu_stack:
            self.menu_stack[-1].update()

    def draw(self, screen: pygame.Surface) -> None:
        if self.menu_stack:
            self.menu_stack[-1].draw(screen)

    def handle_keydown(self, key: int) -> None:
        if self.menu_stack:
            self.menu_stack[-1].handle_keydown(key)

    def has_menu(self) -> bool:
        return len(self.menu_stack) > 0
