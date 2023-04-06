import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.game import Game


class Menu(pygame.sprite.Sprite):
    def __init__(
        self,
        game: "Game",
        options: list[tuple[str, callable]],  # type:ignore
        title: str,
    ) -> None:
        self.options = options
        self.current_option = 0

        self.game = game
        self.colors = game.settings["colors"]

        self.title = title

    def draw(self, screen: pygame.Surface) -> None:
        width, height = screen.get_size()
        option_height = height // (len(self.options) + 1)

        title_surface = self.game.font.render(self.title, True, self.colors["title"])
        title_rect = title_surface.get_rect()
        title_rect.center = width // 2, option_height // 2
        screen.blit(title_surface, title_rect)

        for i, (option_text, _) in enumerate(self.options):
            color = (
                self.colors["selected"]
                if i == self.current_option
                else self.colors["text"]
            )
            option_surface = self.game.font.render(option_text, True, color)
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
            ("Налаштування", game.show_settings_menu),
            ("Вийти", game.quit),
        ]
        super().__init__(game, options, "PACMAN")  # type: ignore


class PauseMenu(Menu):
    def __init__(self, game: "Game") -> None:
        options = [
            ("Продовжити", game.resume),
            ("Нова гра", game.restart),
            ("Налаштування", game.show_settings_menu),
            ("Вийти", game.quit),
        ]
        super().__init__(game, options, "Пауза")  # type: ignore


class EndMenu(Menu):
    def __init__(self, game: "Game") -> None:
        options = [
            ("Перезапустити", game.restart),
            ("Вийти", game.quit),
        ]
        super().__init__(game, options, "Кінець гри")  # type: ignore


class SettingsMenu(Menu):
    def __init__(self, game: "Game") -> None:
        self.screen_sizes = ["1920x1080", "800x800"]
        self.font_sizes = ["Small", "Medium", "Large", "Huge"]
        self.font_size_values = [12, 24, 36, 48]

        self.current_screen_size = self.get_current_screen_size_index(game)
        self.current_font_size = self.get_current_font_size_index(game)

        options = [
            (self.get_screen_size_text(), self.change_screen_size),
            (self.get_font_size_text(), self.change_font_size),
            ("Зберегти та повернутися", self.save_and_return),
            ("Повернутися", game.show_previous_menu),
        ]
        super().__init__(game, options, "Налаштування")  # type: ignore

    def change_font_size(self) -> None:
        self.current_font_size = (self.current_font_size + 1) % len(self.font_sizes)
        self.options[1] = (self.get_font_size_text(), self.change_font_size)

    def change_screen_size(self) -> None:
        self.current_screen_size = (self.current_screen_size + 1) % len(
            self.screen_sizes
        )
        self.options[0] = (self.get_screen_size_text(), self.change_screen_size)

    def save_and_return(self) -> None:
        screen_size = [
            int(dim) for dim in self.screen_sizes[self.current_screen_size].split("x")
        ]
        font_size = self.font_size_values[self.current_font_size]

        width, height = screen_size
        self.game.settings["screen"]["width"] = width
        self.game.settings["screen"]["height"] = height
        self.game.settings["font"]["size"] = font_size
        self.game.settings.save()

        self.game.resize_screen(width, height)
        self.game.resize_font(font_size)

        self.game.show_previous_menu()

    def get_current_screen_size_index(self, game: "Game") -> int:
        return self.screen_sizes.index(
            f"{game.settings['screen']['width']}x{game.settings['screen']['height']}"
        )

    def get_current_font_size_index(self, game: "Game") -> int:
        return self.font_size_values.index(game.settings["font"]["size"])

    def get_screen_size_text(self) -> str:
        return f"Розмір екрану: {self.screen_sizes[self.current_screen_size]}"

    def get_font_size_text(self) -> str:
        return f"Розмір шрифту: {self.font_sizes[self.current_font_size]}"
