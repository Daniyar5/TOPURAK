import json
import os
from src.core.window import window, width, height, new_form
from src.entities.player import Player
from src.world.level import Level
from src.world.map import level_1_layers, level_2_layers
from src.core.camera import Camera
from src.entities.block import TEXTURES
from src.ui.loss import Loss

TILE_SIZE = 16 * new_form
level = None
current_level = 1
player = Player('assets/sprites/player/move', 0, 0, 6)
camera = Camera(width, height, 0.08)

class Game:
    checkpoint_inventory = []
    state = "playing"
    loss_screen = None
    def __init__(self):
        Game.load_level(1)

    @staticmethod
    def load_level(level_num, is_respawn=False):
        global level, current_level
        current_level = level_num
        Game.state = "playing"

        if level_num == 1:
            layers = level_1_layers
        elif level_num == 2:
            layers = level_2_layers
        else:
            print("Поздравляем, игра пройдена! Других уровней пока нет.")
            return

        level = Level(layers, TILE_SIZE)
        spawn_x, spawn_y = level.player_spawn
        player.set_position(spawn_x, spawn_y)
        camera.x = player.rect.centerx - camera.width / 2
        camera.y = player.rect.centery - camera.height / 2

        if not is_respawn:
            Game.checkpoint_inventory = player.inventory.copy()
            Game.save_to_file()
        else:
            player.inventory = Game.checkpoint_inventory.copy()
    
    @staticmethod
    def save_to_file():
        save_data = {
            "current_level": current_level,
            "inventory": Game.checkpoint_inventory
        }
        with open("savegame.json", "w") as f:
            json.dump(save_data, f)
        print(f"--- Игра сохранена! Уровень: {current_level} ---")

    @staticmethod
    def load_from_file():
        if os.path.exists("savegame.json"):
            with open("savegame.json", "r") as f:
                save_data = json.load(f)
            player.inventory = save_data["inventory"]
            Game.load_level(save_data["current_level"])
            print("--- Сохранение успешно загружено! ---")
        else:
            print("Файл сохранения не найден, начинаем новую игру.")
            Game.load_level(1)

    @staticmethod
    def update_and_draw(events):
        global level, current_level
        if level is None:
            return
        if Game.state == "game_over":
            action = Game.loss_screen.draw(events)
            if action == "respawn":
                Game.load_level(current_level, is_respawn=True)
            return
        player.move(level.rects)
        if player.check_pits(level.pit_rects) == "fall":
            Game.state = "game_over" 
            if Game.loss_screen is None:
                Game.loss_screen = Loss()
            Game.loss_screen.reset()
            return
        
        action = player.interact(level.items, level.props)
        if action == "next_level":
            Game.load_level(current_level + 1)
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
