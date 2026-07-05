from src.utils.assets import load_image
from src.core.window import window

class Title:
    def __init__(self, path_img, x, y):
        self.title = load_image(path_img)
        self.rect = self.title.get_rect(center=(x, y))

    def draw(self):
        window.blit(self.title, (self.rect.x, self.rect.y))