import pygame
from settings import ISettings


class UI:
    def __init__(self, font: pygame.font.Font, settings: ISettings) -> None:
        self.font = font
        self.settings = settings

    def display_score(self, screen: pygame.Surface, score: int) -> None:
        """
        Відображає поточний рахунок гравця.
        """

        score_text = self.font.render(
            f"Score: {score}", True, self.settings["colors"]["text"]
        )
        screen.blit(score_text, [0, 30])

    def display_level(self, screen: pygame.Surface, level: int) -> None:
        """
        Відображає поточний рівень гри.
        """

        level_text = self.font.render(
            f"Level: {level}", True, self.settings["colors"]["text"]
        )
        screen.blit(level_text, [0, 0])
