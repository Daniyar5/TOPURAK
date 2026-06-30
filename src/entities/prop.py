import pygame
from src.entities.block import Block

class Prop(Block):
    def __init__(self, x, y, tile_size, block_type):
        super().__init__(x, y, block_type)
        self.rect.bottomleft = (x, y + tile_size)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)
        self.hitbox.midbottom = self.rect.midbottom
        self.pos = pygame.math.Vector2(self.hitbox.bottomleft)