import json, os
from src.core.window import window, width, height, new_form
from src.entities.player import Player
from src.world.level import Level
from src.core.camera import Camera
from src.entities.textures import TEXTURES
from src.ui.loss import Loss

TILE_SIZE = 16 * new_form

class Game:
    def __init__(self):
        self.current_level = 1
        self.level = None
        self.player = Player('assets/sprites/player/move', 0, 0, 6)
        self.camera = Camera(width, height, 0.08)
        
        self.checkpoint_inventory = []
        self.state = "playing"
        self.loss_screen = None
        
        self.load_level(1)

    def load_level(self, level_num, is_respawn=False):
        self.current_level = level_num
        self.state = "playing"

        if level_num == 1:
            self.level = Level("assets/maps/level_1.tmx")
        elif level_num == 2:
            self.level = Level("assets/maps/level_2.tmx")
        else:
            print("Поздравляем, игра пройдена! Других уровней пока нет.")
            return

        spawn_x, spawn_y = self.level.player_spawn
        self.player.set_position(spawn_x, spawn_y)
        self.camera.x = self.player.rect.centerx - self.camera.width / 2
        self.camera.y = self.player.rect.centery - self.camera.height / 2

        if not is_respawn:
            self.checkpoint_inventory = self.player.inventory.copy()
            self.save_to_file()
        else:
            self.player.inventory = self.checkpoint_inventory.copy()
    
    def save_to_file(self):
        save_data = {
            "current_level": self.current_level,
            "inventory": self.checkpoint_inventory
        }
        with open("savegame.json", "w") as f:
            json.dump(save_data, f)
        print(f"--- Игра сохранена! Уровень: {self.current_level} ---")

    def load_from_file(self):
        if os.path.exists("savegame.json"):
            with open("savegame.json", "r") as f:
                save_data = json.load(f)
            self.player.inventory = save_data["inventory"]
            self.load_level(save_data["current_level"])
            print("--- Сохранение успешно загружено! ---")
        else:
            print("Файл сохранения не найден, начинаем новую игру.")
            self.load_level(1)

    def update_and_draw(self, events):
        if self.level is None:
            return
            
        # Проверка проигрыша
        if self.state == "game_over":
            action = self.loss_screen.draw(events)
            if action == "respawn":
                self.load_level(self.current_level, is_respawn=True)
            return
            
        # Обычная логика игры
        self.player.move(self.level.rects, self.camera)
        
        if self.player.check_pits(self.level.pit_rects) == "fall":
            self.state = "game_over" 
            if self.loss_screen is None:
                self.loss_screen = Loss()
            self.loss_screen.reset()
            return
        
        action = self.player.interact(self.level.items, self.level.props)
        if action == "next_level":
            self.load_level(self.current_level + 1)
            return
        
        self.camera.update(self.player)
        self.player.animated()

        # Отрисовка
        window.fill((0, 0, 0))
        self.level.draw_background(self.camera)
        
        ysort_queue = self.level.props + [self.player]
        ysort_queue.sort(key=lambda sprite: sprite.rect.bottom)
        for sprite in ysort_queue:
            sprite.draw(self.camera)

        self.level.draw_items(self.camera)
        self.level.draw_foreground(self.camera)
        self.draw_ui()

    def draw_ui(self):
        x_offset = 20
        y_offset = 20
        for item_type in self.player.inventory:
            img = TEXTURES[item_type]
            window.blit(img, (x_offset, y_offset))
            y_offset += img.get_height() + 10