import toml


class Settings:
    def __init__(self, config_file="settings.toml"):
        self.config = toml.load(config_file)

        self.screen = self.config["screen"]
        self.colors = self.config["colors"]
        self.font = self.config["font"]
        self.controls = self.config["controls"]
        
        self.wall = self.config["wall"]
        self.pacman = self.config["pacman"]
        self.ghost = self.config["ghost"]
        self.food = self.config["food"]
        
        self.levels = self.config["levels"]
