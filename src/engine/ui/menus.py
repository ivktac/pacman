from typing import Callable
from enum import IntEnum
import pygame

from engine.settings import JsonSettings


class MenuOption:
    def __init__(self, label: str, action: Callable) -> None:
        self.__label = label
        self.__action = action

    def __call__(self) -> None:
        self.__action()

    def __str__(self) -> str:
        return self.__label

    def change_label(self, label: str) -> None:
        self.__label = label


class BaseMenu(pygame.sprite.Sprite):
    def __init__(
        self,
        font: pygame.font.Font,
        colors: dict[str, str],
        title: str = "",
    ) -> None:
        super().__init__()

        self.__selected = 0
        self.__options: list[MenuOption] = []

        self.__font = font
        self.__title_color = colors.get("title", "blue")
        self.__text_color = colors.get("text", "white")
        self.__selected_color = colors.get("selected", "yellow")

        self.__title = title

    def draw(self, screen: pygame.Surface) -> None:
        width, height = screen.get_size()
        option_height = height // (len(self.__options) + 1)

        self.draw_title(screen, width, option_height)
        self.draw_options(screen, width, option_height)

    def add_option(self, option: MenuOption) -> None:
        self.__options.append(option)

    def change_option_label(self, index: int, label: str) -> None:
        self.__options[index].change_label(label)

    def change_font(self, font: pygame.font.Font) -> None:
        self.__font = font

    def change_title(self, title: str) -> None:
        self.__title = title

    def handle_keydown(self, key: int) -> None:
        match key:
            case pygame.K_UP:
                self.next_option(-1)
            case pygame.K_DOWN:
                self.next_option(1)
            case pygame.K_RETURN:
                self.__options[self.__selected]()

    def next_option(self, value: int) -> None:
        self.__selected = (self.__selected + value) % len(self.__options)

    def draw_title(self, screen: pygame.Surface, width: int, height: int) -> None:
        title_surface = self.__font.render(self.__title, True, self.__title_color)

        title_rect = title_surface.get_rect()
        title_rect.center = width // 2, height // 2

        screen.blit(title_surface, title_rect)

    def draw_options(self, screen: pygame.Surface, width: int, height: int) -> None:
        for i, option in enumerate(self.__options):
            color = self.__selected_color if i == self.__selected else self.__text_color

            option_surface = self.__font.render(str(option), True, color)

            option_rect = option_surface.get_rect()
            option_rect.center = width // 2, (i + 1) * height

            screen.blit(option_surface, option_rect)

    def __str__(self) -> str:
        return self.__title


class MenuState(IntEnum):
    MAIN = 0
    SETTINGS = 1
    PAUSE = 2
    NEW_RECORD = 3
    GAME_OVER = 4


class MenuGroup(pygame.sprite.Group):
    def __init__(self, *sprites: BaseMenu) -> None:
        super().__init__(*sprites)

        self.__stack = []
        self.__current: int | None = None

    def handle_keydown(self, key: int) -> None:
        if self.__current is not None:
            self.sprites()[self.__current].handle_keydown(key)

    def add_option(self, index: int, option: MenuOption) -> None:
        self.sprites()[index].add_option(option)

    def open_menu(self, index: int) -> None:
        self.__stack.append(self.__current)
        self.__current = index

    def close_menu(self) -> None:
        self.__current = self.__stack.pop() if self.__stack else None

    def draw(self, screen: pygame.Surface) -> None:
        if self.__current is not None:
            self.sprites()[self.__current].draw(screen)

    def __getitem__(self, index: int) -> BaseMenu:
        return self.sprites()[index]

    def update(self) -> None:
        ...

    def __bool__(self) -> bool:
        return self.__current is not None


class MenuInterface:
    def __init__(self, callbacks: dict[str, Callable]) -> None:
        self.__callbacks = callbacks

        self.__fonts = {
            "Малий": pygame.font.SysFont("monospace", 30),
            "Середній": pygame.font.SysFont("monospace", 40),
            "Великий": pygame.font.SysFont("monospace", 50),
        }

        self.__settings = JsonSettings("data/settings.json")
        self.__settings.load()

        self.__font_size_name = self.__settings.get("font", "Середній")
        self.__font = self.__fonts[self.__font_size_name]

        self.__colors = {"title": "blue", "text": "white", "selected": "yellow"}

        self.__menus = MenuGroup(
            BaseMenu(self.__font, self.__colors, "Головне меню"),
            BaseMenu(self.__font, self.__colors, "Налаштування"),
            BaseMenu(self.__font, self.__colors, "Пауза"),
            BaseMenu(self.__font, self.__colors, "Результат"),
            BaseMenu(self.__font, self.__colors, "Кінець гри"),
        )

        self.__menus.add_option(
            MenuState.PAUSE, MenuOption("Продовжити", self.__resume_game)
        )

        for state in [
            MenuState.MAIN,
            MenuState.PAUSE,
            MenuState.NEW_RECORD,
            MenuState.GAME_OVER,
        ]:
            self.__menus.add_option(state, MenuOption("Нова гра", self.__start_game))
            self.__menus.add_option(
                state, MenuOption("Налаштування", self.open_settings)
            )
            self.__menus.add_option(state, MenuOption("Вийти", self.__quit_game))

        self.__menus.add_option(
            MenuState.SETTINGS,
            MenuOption(
                f"Змінити розмір шрифту: {self.__font_size_name}",
                self.__change_font_size,
            ),
        )

        self.__menus.add_option(
            MenuState.SETTINGS, MenuOption("Зберегти", self.__save_settings)
        )
        self.__menus.add_option(
            MenuState.SETTINGS, MenuOption("Повернутися", self.open_previous)
        )

    def get_font(self) -> pygame.font.Font:
        return self.__font

    def update(self) -> None:
        self.__menus.update()

    def draw(self, screen: pygame.Surface) -> None:
        self.__menus.draw(screen)

    def open_settings(self) -> None:
        self.__menus.open_menu(MenuState.SETTINGS)

    def open_previous(self) -> None:
        self.__menus.close_menu()

    def open_pause(self) -> None:
        self.__menus.open_menu(MenuState.PAUSE)

    def open_game_over(self) -> None:
        self.__menus.open_menu(MenuState.GAME_OVER)

    def open_new_record(self, score: int) -> None:
        if score > self.__settings.get("score", 0):
            self.__settings.set("score", score)
            self.__settings.save()

        new_title = f"Ваш результат: {score}"

        self.__menus[MenuState.NEW_RECORD].change_title(new_title)
        self.__menus.open_menu(MenuState.NEW_RECORD)

    def open_main(self) -> None:
        self.__menus[MenuState.MAIN].change_title(
            f"Рекорд: {self.__settings.get('score', 0)}"
        )
        self.__menus.open_menu(MenuState.MAIN)

    def close(self) -> None:
        self.__menus.close_menu()

    def is_open(self) -> bool:
        return bool(self.__menus)

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE and not self.is_open():
            self.open_pause()

        self.__menus.handle_keydown(key)

    def __start_game(self) -> None:
        self.__callbacks["start"]()

    def __quit_game(self) -> None:
        self.__callbacks["quit"]()

    def __resume_game(self) -> None:
        self.__callbacks["resume"]()

    def __change_font_size(self) -> None:
        font_sizes = list(self.__fonts.keys())
        index = font_sizes.index(self.__font_size_name)
        self.__font_size_name = font_sizes[(index + 1) % len(font_sizes)]

        self.__menus[MenuState.SETTINGS].change_option_label(
            0, f"Змінити розмір шрифту: {self.__font_size_name}"
        )

    def __save_settings(self) -> None:
        self.__settings.set("font", self.__font_size_name)
        self.__font = self.__fonts[self.__font_size_name]

        for menu in self.__menus:
            menu.change_font(self.__font)

        self.__settings.save()
