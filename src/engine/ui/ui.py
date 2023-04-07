import pygame


class UI:
    def __init__(self) -> None:
        self.__heart_image = pygame.image.load("assets/images/heart.png")
        self.__heart_image = pygame.transform.scale(self.__heart_image, (64, 64))

    def display(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        score: int,
        level: int,
        health: int,
    ) -> None:
        self.__display_score(screen, font, score)
        self.__display_level(screen, font, level)
        self.__display_health(screen, health)

    def __display_score(
        self, screen: pygame.Surface, font: pygame.font.Font, score: int
    ) -> None:
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, [0, 30])

    def __display_level(
        self, screen: pygame.Surface, font: pygame.font.Font, level: int
    ) -> None:
        level_text = font.render(f"Level: {level}", True, "white")
        screen.blit(level_text, [0, 60])

    def __display_health(self, screen: pygame.Surface, health: int) -> None:
        for i in range(health):
            screen.blit(self.__heart_image, [i * 32, -10])
