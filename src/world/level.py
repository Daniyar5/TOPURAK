import pygame, pytmx
from src.core.window import window, new_form

class Level:
    def __init__(self, tmx_file_path):
        self.tmx_data = pytmx.load_pygame(tmx_file_path)
        self.tile_size = self.tmx_data.tilewidth * new_form

        self.scaled_tiles = {}
        self.rects = []
        self.pit_rects = []
        self.player_spawn = (0, 0)
        self.items = []
        self.props = []

        self._parse_level()

    # Вспомогательная функция: правильно увеличивает любую картинку
    def get_scaled_tile(self, gid):
        if gid not in self.scaled_tiles:
            img = self.tmx_data.get_tile_image_by_gid(gid)
            if img:
                new_w = img.get_width() * new_form
                new_h = img.get_height() * new_form
                scaled_img = pygame.transform.scale(img, (new_w, new_h))
                self.scaled_tiles[gid] = scaled_img
            else:
                self.scaled_tiles[gid] = None
                
        return self.scaled_tiles[gid]

    def _parse_level(self):
        for layer in self.tmx_data.objectgroups:
            print(f"--- Проверяем слой объектов: '{layer.name}' ---")
            
            if layer.name == 'collisions':
                for obj in layer:
                    rect = pygame.Rect(
                        obj.x * new_form, 
                        obj.y * new_form, 
                        obj.width * new_form, 
                        obj.height * new_form
                    )
                    self.rects.append(rect)
                    
            elif layer.name == 'logic':
                for obj in layer:
                    if obj.name == 'player_spawn':
                        self.player_spawn = (obj.x * new_form, obj.y * new_form)
            
            elif layer.name == 'props':
                for obj in layer:
                    if hasattr(obj, 'gid') and obj.gid:
                        img = self.tmx_data.get_tile_image_by_gid(obj.gid)
                        
                        if img:
                            new_w = img.get_width() * new_form
                            new_h = img.get_height() * new_form
                            scaled_img = pygame.transform.scale(img, (new_w, new_h))
                            
                            x_pos = obj.x * new_form
                            y_pos = obj.y * new_form

                            prop_type = obj.name if obj.name else "prop"
                            
                            new_prop = TiledSprite(x_pos, y_pos, scaled_img, prop_type)
                            self.props.append(new_prop)
                            print(f"Успех! Мебель встала на место: x={x_pos}, y={y_pos}")
                        else:
                            print("Ошибка: Найдена пустая мебель без картинки!")
            
            elif layer.name == 'items':
                for obj in layer:
                    if hasattr(obj, 'gid') and obj.gid:
                        img = self.tmx_data.get_tile_image_by_gid(obj.gid)
                        if img:
                            new_w = img.get_width() * new_form
                            new_h = img.get_height() * new_form
                            scaled_img = pygame.transform.scale(img, (new_w, new_h))
                            
                            x_pos = obj.x * new_form
                            y_pos = obj.y * new_form
                            
                            item_type = obj.name if obj.name else "key"
                            
                            new_item = TiledSprite(x_pos, y_pos, scaled_img, item_type)
                            self.items.append(new_item)
                            print(f"Успех! Предмет '{item_type}' добавлен на карту.")

            elif layer.name == 'pits':
                for obj in layer:
                    rect = pygame.Rect(
                        obj.x * new_form, 
                        obj.y * new_form, 
                        obj.width * new_form, 
                        obj.height * new_form
                    )
                    self.pit_rects.append(rect)
                    print(f"Добавлена яма на координатах: {rect.x}, {rect.y}")

    def draw_background(self, camera):
        bg_keywords = ['floor', 'objects']
        
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                layer_name_clean = layer.name.lower().strip()
                
                if layer_name_clean in bg_keywords:
                    for x, y, gid in layer:
                        tile_image = self.get_scaled_tile(gid)
                        if tile_image:
                            world_x = x * self.tile_size
                            world_y = y * self.tile_size
                            window.blit(tile_image, (world_x - camera.x, world_y - camera.y))
                        
    def draw_items(self, camera):
        for item in self.items:
            item.draw(camera)

    def draw_foreground(self, camera):
        fg_keywords = ['walls']
        
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                layer_name_clean = layer.name.lower().strip()
                
                if layer_name_clean in fg_keywords:
                    for x, y, gid in layer:
                        tile_image = self.get_scaled_tile(gid)
                        if tile_image:
                            world_x = x * self.tile_size
                            world_y = y * self.tile_size
                            window.blit(tile_image, (world_x - camera.x, world_y - camera.y))

class TiledSprite:
    def __init__(self, x, y, image, obj_type):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = obj_type
        
    def draw(self, camera):
        from src.core.window import window
        window.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))