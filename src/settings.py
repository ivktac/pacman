import toml


class Settings:
    def __init__(self, config_file="settings.toml"):
        self.config = toml.load(config_file)
        self.screen = self.config["screen"]
        self.colors = self.config["colors"]
        self.pacman = self.config["pacman"]
        self.ghost = self.config["ghost"]
