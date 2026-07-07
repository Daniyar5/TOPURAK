import pygame
from src.entities.block import Block, TEXTURES
from src.entities.prop import Prop

class Level:
    def __init__(self, level_layers, tile_size):
        self.background_blocks = []
        self.props = []
        self.foreground_blocks = []
        self.items = []
        self.rects = []
        self.pit_rects = []
        self.tile_size = tile_size
        self.player_spawn = (0, 0)
        solid_types = ['O', 'W', 'Q', 'S', 'T', 'U']
        object_types = ['t', '4', 'R', 'V', 'X', 'Y', 'd', 'c']
        pit_types = ['I']
        open_door_types = ['o']


        foreground_types = []
        item_types = ['k']

        for layer in level_layers:
            for row_idx, row in enumerate(layer):
                for col_idx, char in enumerate(row):
                    x = col_idx * self.tile_size
                    y = row_idx * self.tile_size

                    if char == "P":
                        self.player_spawn = (x, y)
                    elif char in foreground_types and char in TEXTURES:
                        new_block = Block(x, y, char)
                        self.foreground_blocks.append(new_block)
                    elif char in item_types and char in TEXTURES:
                        new_item = Block(x, y, char)
                        self.items.append(new_item)
                    elif char in object_types and char in TEXTURES:
                        new_object = Prop(x, y, self.tile_size, char)
                        self.props.append(new_object)
                        self.rects.append(new_object.hitbox)
                    elif char in open_door_types and char in TEXTURES:
                        new_door = Block(x, y, char)
                        self.props.append(new_door)
                    elif char in pit_types and char in TEXTURES:
                        new_block = Block(x, y, char)
                        self.background_blocks.append(new_block)
                        pit_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                        self.pit_rects.append(pit_rect)
                    elif char in TEXTURES:
                        new_block = Block(x, y, char)
                        self.background_blocks.append(new_block)
                        if char in solid_types:
                            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                            self.rects.append(rect)

    def draw_background(self, camera):
        for block in self.background_blocks:
            block.draw(camera)

    def draw_foreground(self, camera):
        for block in self.foreground_blocks:
            block.draw(camera)
    
    def draw_items(self, camera):
        for item in self.items:
            item.draw(camera)