import pygame
from src.utils.assets import load_image
from src.core.window import window

class Button:
    def __init__(self, path_texture, x, y):
        self.texture = load_image(path_texture)
        self.rect = self.texture.get_rect(center=(x, y))

    def draw(self):
        window.blit(self.texture, (self.rect.x, self.rect.y))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False