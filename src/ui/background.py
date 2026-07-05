from src.utils.assets import load_image
from src.core.window import window

class Background:
    def __init__(self, path_bg):
        self.background = load_image(path_bg)

    def draw(self):
        window.blit(self.background, (0, 0))
