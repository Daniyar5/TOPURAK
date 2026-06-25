import pygame
import math
from src.core.window import window
from src.utils.assets import load_animation_frames

class Player:
    def __init__(self, folder_path, x, y, speed):
        self.animations = {
            'idle': load_animation_frames(folder_path, 'idle'),
            'right': load_animation_frames(folder_path, 'run_right'),
            'left': load_animation_frames(folder_path, 'run_left'),
            'up': load_animation_frames(folder_path, 'run_up'),
            'down': load_animation_frames(folder_path, 'run_down')
        }
        self.skin = self.animations['idle'][0]
        self.rect = self.skin.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-12, -self.rect.height / 2)
        self.hitbox.midbottom = self.rect.midbottom
        self.pos = pygame.math.Vector2(self.hitbox.center)
        self.speed = speed

        self.inventory = []

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.idle_delay = 220
        self.direction = 'idle'
        self.moving = False

    def draw(self, camera):
        current_skin = self.animations[self.direction][self.current_frame]
        window.blit(current_skin, (self.rect.x - camera.x, self.rect.y - camera.y))

    def move(self, solid_rects):
        keys = pygame.key.get_pressed()
        move_dir = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            move_dir.y -= 1
            self.direction = 'up'
        if keys[pygame.K_s]:
            move_dir.y += 1
            self.direction = 'down'
        if keys[pygame.K_a]:
            move_dir.x -= 1
            self.direction = 'left'
        if keys[pygame.K_d]:
            move_dir.x += 1
            self.direction = 'right'

        if move_dir.length_squared() > 0:
            move_dir = move_dir.normalize()
            self.moving = True
        else:
            self.moving = False
            self.direction = 'idle'

        # Столкновение
        self.pos.x += move_dir.x * self.speed
        self.hitbox.centerx = round(self.pos.x)

        for rect in solid_rects:
            if self.hitbox.colliderect(rect):
                if move_dir.x > 0:
                    self.hitbox.right = rect.left
                if move_dir.x < 0:
                    self.hitbox.left = rect.right
                self.pos.x = self.hitbox.centerx

        self.pos.y += move_dir.y * self.speed
        self.hitbox.centery = round(self.pos.y)

        for rect in solid_rects:
            if self.hitbox.colliderect(rect):
                if move_dir.y > 0:
                    self.hitbox.bottom = rect.top
                if move_dir.y < 0:
                    self.hitbox.top = rect.bottom
                self.pos.y = self.hitbox.centery

        self.rect.midbottom = self.hitbox.midbottom

    def animated(self):
        current_target_time = self.animation_speed
        if self.direction == 'idle' and self.current_frame == 0:
            current_target_time = self.idle_delay
        self.animation_timer += 1
        if self.animation_timer >= current_target_time:
            self.animation_timer = 0
            current_anim_length = len(self.animations[self.direction])
            self.current_frame = (self.current_frame + 1) % current_anim_length

    def set_position(self, x, y):
        self.rect.topleft = (x, y)
        self.hitbox = self.rect.inflate(-10, -self.rect.height / 2)
        self.hitbox.midbottom = self.rect.midbottom 
        self.pos = pygame.math.Vector2(self.hitbox.center)

    def interact(self, items, props):
        keys = pygame.key.get_pressed()   
        if keys[pygame.K_e]:
            for item in items[:]: 
                dist = math.hypot(self.rect.centerx - item.rect.centerx, self.rect.centery - item.rect.centery)
                if dist < 150:
                    self.inventory.append(item.type)
                    items.remove(item)
            
            for prop in props:
                if prop.type == "c": 
                    dist = math.hypot(self.rect.centerx - prop.rect.centerx, self.rect.centery - prop.rect.centery)
                    if dist < 180:
                        if "k" in self.inventory:
                            self.inventory.remove("k")
                            return "next_level"
        return None
    
    def check_pits(self, pit_rects):
        for pit in pit_rects:
            if pit.collidepoint(self.hitbox.center):
                return "fall"
                
        return None