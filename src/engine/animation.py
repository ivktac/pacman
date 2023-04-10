from typing import Any

import pygame


class Animation:
    def __init__(
        self, animations_config: dict[str, dict[str, Any]], size: tuple[int, int]
    ) -> None:
        self.animations = {}

        for animation_name, config in animations_config.items():
            image = pygame.image.load(config["image_path"]).convert_alpha()
            frames = self.__split_frames(image, size, config["num_frames"])
            self.animations[animation_name] = frames

        self.__frame_counters = {animation: 0 for animation in animations_config}
        self.current_frames = {animation: 0 for animation in animations_config}

    def get_current_frame(self, animation_name: str) -> pygame.Surface:
        return self.animations[animation_name][self.current_frames[animation_name]]

    def update_frame(self, animation_name: str, frame_delay: int) -> None:
        self.__frame_counters[animation_name] += 1

        if self.__frame_counters[animation_name] > frame_delay:
            self.__frame_counters[animation_name] = 0

            num_frames = len(self.animations[animation_name])

            self.current_frames[animation_name] = (
                self.current_frames[animation_name] + 1
            ) % num_frames

    def __split_frames(
        self, image: pygame.Surface, frame_size: tuple[int, int], num_frames: int
    ) -> list[pygame.Surface]:
        frame_width, frame_height = frame_size

        frames = []
        for i in range(num_frames):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames
