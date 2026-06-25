import pygame
from src.core.window import window
from src.utils.assets import load_image

class Button:
    def __init__(self, x, y, texture_path):
        self.texture = load_image(texture_path)
        self.rect = self.texture.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    def draw(self):
        window.blit(self.texture, (self.pos.x, self.pos.y))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False