from typing import Callable
from enum import IntEnum
import pygame

from engine.settings import SettingsManager


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

    def __add__(self, other: BaseMenu):
        self.add(other)
        return self


class Menu:
    def __init__(
        self,
        callbacks: dict[str, Callable],
        settings_manager: SettingsManager,
    ) -> None:
        self.__colors = {"title": "blue", "text": "white", "selected": "yellow"}
        self.__callbacks = callbacks
        self.__settings_manager = settings_manager

        self.__font_size = self.__settings_manager.get_font_size()
        self.__font = self.__settings_manager.get_font()

        self.__menus = MenuGroup(BaseMenu(self.__font, self.__colors, "Головне меню"))

        self.__menus += BaseMenu(self.__font, self.__colors, "Налаштування")
        self.__menus += BaseMenu(self.__font, self.__colors, "Пауза")
        self.__menus += BaseMenu(self.__font, self.__colors, "Новий рекорд")
        self.__menus += BaseMenu(self.__font, self.__colors, "Кінець гри")

        self.__add_options_to_menus(self.__menus)

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
        new_title = f"Ваш результат: {score}"

        if score > self.__settings_manager.get_highscore():
            new_title = f"Новий рекорд: {score}!!!"
            self.__settings_manager.set("highscore", score)
            self.__settings_manager.save()

        self.__menus[MenuState.NEW_RECORD].change_title(new_title)
        self.__menus.open_menu(MenuState.NEW_RECORD)

    def open_main(self) -> None:
        self.__menus[MenuState.MAIN].change_title(
            f"Рекорд: {self.__settings_manager.get_highscore()}"
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

    def __add_options_to_menus(self, menus: MenuGroup) -> None:
        menus.add_option(MenuState.PAUSE, MenuOption("Продовжити", self.__resume_game))

        self.__add_default_options(menus[MenuState.MAIN])
        self.__add_default_options(menus[MenuState.PAUSE])
        self.__add_default_options(menus[MenuState.GAME_OVER])
        self.__add_default_options(menus[MenuState.NEW_RECORD])

        self.__add_settings_options(menus[MenuState.SETTINGS])

    def __add_default_options(self, menu: BaseMenu) -> None:
        menu.add_option(MenuOption("Нова гра", self.__start_game))
        menu.add_option(MenuOption("Налаштування", self.open_settings))
        menu.add_option(MenuOption("Вийти", self.__quit_game))

    def __add_settings_options(self, menu: BaseMenu) -> None:
        menu.add_option(MenuOption("Змінити розмір шрифт", self.__change_font_size))
        menu.add_option(MenuOption("Зберегти", self.__save_settings))
        menu.add_option(MenuOption("Назад", self.open_previous))

    def __start_game(self) -> None:
        self.__callbacks["start"]()

    def __quit_game(self) -> None:
        self.__callbacks["quit"]()

    def __resume_game(self) -> None:
        self.__callbacks["resume"]()

    def __change_font_size(self) -> None:
        names = self.__settings_manager.get_font_size_names()
        self.__font_size = names[(names.index(self.__font_size) + 1) % len(names)]

        self.__menus[MenuState.SETTINGS].change_option_label(
            0, f"Змінити розмір шрифт: {self.__font_size}"
        )

    def __change_font(self) -> None:
        self.__font = self.__settings_manager.get_font()

        for menu in self.__menus.sprites():
            if type(menu) is not BaseMenu:
                continue
            menu.change_font(self.__font)

    def __save_settings(self) -> None:
        self.__settings_manager.set("font", self.__font_size)
        self.__settings_manager.save()

        self.__change_font()

        self.open_previous()
