import pygame

from engine.settings import ISettings


class UI:
    def __init__(self, font: pygame.font.Font, settings: ISettings) -> None:
        self.font = font
        self.settings = settings

        self.heart_image = pygame.image.load("assets/images/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (64, 64))

    def display_score(self, screen: pygame.Surface, score: int) -> None:
        score_text = self.font.render(
            f"Score: {score}", True, self.settings["colors"]["text"]
        )
        screen.blit(score_text, [0, 30])

    def display_level(self, screen: pygame.Surface, level: int) -> None:
        level_text = self.font.render(
            f"Level: {level}", True, self.settings["colors"]["text"]
        )
        screen.blit(level_text, [0, 60])

    def display_health(self, screen: pygame.Surface, health: int) -> None:
        for i in range(health):
            screen.blit(self.heart_image, [i * 32, -10])
