from src.core.window import window
from src.utils.assets import load_block_image

TEXTURES = {
    # Блоки
    "1": load_block_image('assets/sprites/blocks/stone_floor_1.png'),
    "2": load_block_image('assets/sprites/blocks/stone_floor_2.png'),
    "3": load_block_image('assets/sprites/blocks/stone_floor_3.png'),
    "5": load_block_image('assets/sprites/blocks/cover_1.png'),
    "6": load_block_image('assets/sprites/blocks/cover_2.png'),
    "7": load_block_image('assets/sprites/blocks/cover_3.png'),
    "8": load_block_image('assets/sprites/blocks/cover_4.png'),
    "9": load_block_image('assets/sprites/blocks/cover_5.png'),
    "A": load_block_image('assets/sprites/blocks/cover_6.png'),
    "B": load_block_image('assets/sprites/blocks/cover_7.png'),
    "C": load_block_image('assets/sprites/blocks/cover_8.png'),
    "D": load_block_image('assets/sprites/blocks/cover_9.png'),
    "E": load_block_image('assets/sprites/blocks/cover_10.png', True),
    "F": load_block_image('assets/sprites/blocks/cover_11.png', True),
    "G": load_block_image('assets/sprites/blocks/cover_12.png', True),
    "H": load_block_image('assets/sprites/blocks/cover_13.png', True),
    "I": load_block_image('assets/sprites/blocks/pit.png'),
    "J": load_block_image('assets/sprites/blocks/stone_floor_v2_1.png'),
    "K": load_block_image('assets/sprites/blocks/stone_floor_v2_2.png'),
    "L": load_block_image('assets/sprites/blocks/stone_floor_v2_3.png'),
    "M": load_block_image('assets/sprites/blocks/stone_floor_v2_4.png'),
    "N": load_block_image('assets/sprites/blocks/ladder.png'),

    # Стены
    "4": load_block_image('assets/sprites/blocks/brick.png'),
    "O": load_block_image('assets/sprites/blocks/brick_right_1.png', True),
    "W": load_block_image('assets/sprites/blocks/brick_right_2.png', True),
    "Q": load_block_image('assets/sprites/blocks/brick_right_3.png', True),
    "R": load_block_image('assets/sprites/blocks/brick_right_4.png', True),
    "X": load_block_image('assets/sprites/blocks/brick_right_5.png', True),
    "S": load_block_image('assets/sprites/blocks/brick_left_1.png', True),
    "T": load_block_image('assets/sprites/blocks/brick_left_2.png', True),
    "U": load_block_image('assets/sprites/blocks/brick_left_3.png', True),
    "V": load_block_image('assets/sprites/blocks/brick_left_4.png', True),
    "Y": load_block_image('assets/sprites/blocks/brick_left_5.png', True),

    # Объекты
    "d": load_block_image('assets/sprites/objects/door_1.png', True),
    "c": load_block_image('assets/sprites/objects/door_2.png', True),

    # Мебель
    "t": load_block_image('assets/sprites/furnitures/table.png', True),

    # Предметы
    "k": load_block_image('assets/sprites/items/kay_gold.png', True)
}

class Block:
    def __init__(self, x, y, block_type):
        self.type = block_type
        self.image = TEXTURES[block_type]
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, camera):
        window.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))