import sys
import pygame
from engine.settings import JsonSettings, SettingsManager

from entities.player import Player
from engine.level import Level
from engine.ui.menus import Menu
from engine.ui.ui import UI


class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.mixer.init()

        pygame.display.set_caption("Pacman")

        pygame.mixer.music.load("assets/sounds/music.wav")
        pygame.mixer.music.set_volume(0.3)

        self.__settings = SettingsManager(JsonSettings("data/settings.json"))
        self.__settings.load()

        self.__screen = pygame.display.set_mode(
            self.__settings.get_size(), pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self.__background_image = pygame.image.load(
            "assets/images/background.jpg"
        ).convert()
        self.__background_image = pygame.transform.scale(
            self.__background_image, self.__settings.get_size()
        )

        self.__clock = pygame.time.Clock()

        self.__current_level = 1

        self.__player: Player = Player(-100, -100)

        self.__menu = Menu(
            {"start": self.start, "quit": self.quit, "resume": self.resume},
            self.__settings,
        )
        self.__menu.open_main()

        self.__is_paused = False
        self.__is_running = True

        self.__is_sound_enabled = self.__settings.get_sound_enabled()

        self.__is_debug = True

        self.__level: Level | None = None
        self.__ui = UI()

    def run(self) -> None:
        while self.__is_running:
            self.__is_sound_enabled = self.__settings.get_sound_enabled()

            self.soundtrack()

            self.handle_events()

            self.update()

            self.clear_screen()

            self.draw()

            pygame.display.flip()

            self.__clock.tick(60)

    def soundtrack(self) -> None:
        if self.__is_sound_enabled:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.unpause()

            if self.__level:
                self.__level.enable_sound()
        else:
            pygame.mixer.music.pause()

            if self.__level:
                self.__level.disable_sound()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.KEYDOWN:
                    if self.__is_debug:
                        self.debug_handle_keydown(event.key)
                    self.__menu.handle_keydown(event.key)
                    self.__player.handle_keydown(event.key)

    def update(self) -> None:
        if self.__level is None:
            return

        if self.__menu.is_open():
            self.__menu.update()
            return            

        if self.__player.dead() and self.__player.time_since_death() > 3500:
            self.__menu.open_new_record(self.__player.score())
            self.__player = Player(-100, -100)
            return

        if self.__level.is_completed():
            self.load_level(self.__current_level + 1)
            return

        self.__level.update()

    def draw(self) -> None:
        if self.__menu.is_open():
            self.__menu.draw(self.__screen)
            return

        if self.__level:
            self.__level.draw(self.__screen)

        self.__ui.display(
            self.__screen,
            self.__settings.get_font(),
            self.__player.score(),
            self.__current_level,
            self.__player.health(),
        )

    def clear_screen(
        self,
    ) -> None:
        self.__screen.blit(self.__background_image, (0, 0))

    def start(self) -> None:
        self.__menu.close()
        self.__is_paused = False

        self.__player = Player(-100, -100)

        self.__current_level = 1

        self.load_level(self.__current_level)

    def pause(self) -> None:
        self.__is_paused = True
        self.__menu.open_pause()

    def toggle_pause(self) -> None:
        if self.__is_paused:
            self.resume()
        else:
            self.pause()

    def resume(self) -> None:
        self.__is_paused = False
        self.__menu.close()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def load_level(self, level: int) -> None:
        try:
            self.__current_level = level
            self.__level = Level(self.__current_level, self.__player)
        except FileNotFoundError:
            self.__menu.open_game_over()

    def debug_handle_keydown(self, key: int) -> None:
        match key:
            case pygame.K_F1:
                self.start()
            case pygame.K_F2:
                self.load_level(self.__current_level + 1)
            case pygame.K_F3:
                if self.__current_level - 1 < 1:
                    self.load_level(1)
                self.load_level(self.__current_level - 1)
            case pygame.K_F4:
                self.__player.die()
