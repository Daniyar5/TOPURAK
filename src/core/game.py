from src.core.window import window, width, height, new_form
from src.entities.player import Player
from src.world.level import Level
from src.world.map import level_1_layers, level_2_layers
from src.core.camera import Camera
from src.entities.block import TEXTURES

TILE_SIZE = 16 * new_form
level = Level(level_1_layers, TILE_SIZE)
spawn_x, spawn_y = level.player_spawn
player = Player('assets/sprites/player', spawn_x, spawn_y, 15)
camera = Camera(width, height, 0.08)
current_level = 1

class Game:
    def __init__(self):
        pass

    @staticmethod
    def draw():
        global level, current_level
        player.move(level.rects)
        if player.check_pits(level.pit_rects) == "fall":
            print("Game Over! Игрок упал в яму.")
            player.set_position(level.player_spawn[0], level.player_spawn[1])
            camera.x = player.rect.centerx - camera.width / 2
            camera.y = player.rect.centery - camera.height / 2
            return
        
        action = player.interact(level.items, level.props)
        if action == "next_level" and current_level == 1:
            level = Level(level_2_layers, TILE_SIZE)
            new_x = level.player_spawn[0]
            new_y = level.player_spawn[1]
            player.set_position(new_x, new_y)
            camera.x = player.rect.centerx - camera.width / 2
            camera.y = player.rect.centery - camera.height / 2
            current_level = 2
            return
        
        camera.update(player)
        player.animated()

        window.fill((0, 0, 0))
        level.draw_background(camera)
        ysort_queue = level.props + [player]
        ysort_queue.sort(key=lambda sprite: sprite.rect.bottom)
        for sprite in ysort_queue:
            sprite.draw(camera)

        level.draw_items(camera)
        level.draw_foreground(camera)
        Game.draw_ui()

    @staticmethod
    def draw_ui():
        x_offset = 20
        y_offset = 20
        
        for item_type in player.inventory:
            img = TEXTURES[item_type]
            window.blit(img, (x_offset, y_offset))
            y_offset += img.get_height() + 10
