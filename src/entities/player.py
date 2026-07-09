import pygame, math
from src.core.window import window
from src.utils.assets import load_animation_frames, load_image

class Player:
    def __init__(self, folder_path, x, y, speed):
        self.animations = {
            'idle_right': load_animation_frames(folder_path, 'idle_right'),
            'idle_left': load_animation_frames(folder_path, 'idle_left'),
            'idle_down': load_animation_frames(folder_path, 'idle_down'),
            'right': load_animation_frames(folder_path, 'run_right'),
            'left': load_animation_frames(folder_path, 'run_left'),
            'up': load_animation_frames(folder_path, 'run_up'),
            'down': load_animation_frames(folder_path, 'run_down')
        }
        self.aim_image = load_image('assets/sprites/player/aim.png')

        self.skin = self.animations['idle_down'][0]
        self.rect = self.skin.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-12, -self.rect.height / 2)
        self.hitbox.midbottom = self.rect.midbottom
        self.pos = pygame.math.Vector2(self.hitbox.center)

        self.base_speed = speed   
        self.speed = self.base_speed
        
        self.is_dashing = False
        self.is_aiming = False
        self.max_dash_dist = 240
        self.crosshair_pos = pygame.math.Vector2()
        self.dash_dir = pygame.math.Vector2()
        
        self.dash_start_time = 0
        self.dash_duration = 200
        self.last_dash_time = 0
        self.dash_cooldown = 1500

        self.inventory = []

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 60 / 6
        self.idle_delay = 220
        self.direction = 'down'
        self.moving = False

    def draw(self, camera):
        if self.moving or self.is_aiming or self.is_dashing:
            anim_list = self.animations[self.direction]
        else:
            if self.direction == 'up':
                anim_list = self.animations['up']
            else:
                anim_list = self.animations[f'idle_{self.direction}']
        if self.current_frame >= len(anim_list):
            self.current_frame = 0

        current_skin = anim_list[self.current_frame]
        window.blit(current_skin, (self.rect.x - camera.x, self.rect.y - camera.y))

        if self.is_aiming:
            cx = self.crosshair_pos.x - camera.x
            cy = self.crosshair_pos.y - camera.y
            aim_rect = self.aim_image.get_rect(center=(cx, cy))
            window.blit(self.aim_image, aim_rect.topleft)

    def move(self, solid_rects, camera):
        keys = pygame.key.get_pressed()
        move_dir = pygame.math.Vector2(0, 0)
        current_time = pygame.time.get_ticks()

        # Рывок
        shift_pressed = keys[pygame.K_LSHIFT]

        if shift_pressed and not self.is_dashing and (current_time - self.last_dash_time >= self.dash_cooldown):
            self.is_aiming = True
    
            mx, my = pygame.mouse.get_pos()
            world_mx = mx + camera.x
            world_my = my + camera.y
            
            vec = pygame.math.Vector2(world_mx - self.hitbox.centerx, world_my - self.hitbox.centery)
            
            if vec.length() > self.max_dash_dist:
                vec.scale_to_length(self.max_dash_dist)
            
            self.crosshair_pos = pygame.math.Vector2(self.hitbox.centerx, self.hitbox.centery) + vec
            
            if vec.length() > 0:
                angle = math.degrees(math.atan2(vec.y, vec.x))
                if -45 <= angle <= 45:
                    self.direction = 'right'
                elif 45 < angle <= 135:
                    self.direction = 'down'
                elif -135 <= angle < -45:
                    self.direction = 'up'
                else:
                    self.direction = 'left'
        else:
            if self.is_aiming:
                self.is_aiming = False
                self.is_dashing = True
                self.dash_start_time = current_time
                self.last_dash_time = current_time
                
                vec = self.crosshair_pos - pygame.math.Vector2(self.hitbox.centerx, self.hitbox.centery)
                dist = vec.length()
                if dist > 0:
                    self.dash_dir = vec.normalize()
                else:
                    self.dash_dir = pygame.math.Vector2(0, 1)
                
                frames = self.dash_duration / (1000 / 60)
                self.speed = dist / frames

        if self.is_dashing:
            if current_time - self.dash_start_time >= self.dash_duration:
                self.is_dashing = False 
            else:
                move_dir = self.dash_dir

        # Бег туда сюда
        if not self.is_aiming and not self.is_dashing:
            self.speed = self.base_speed
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
        elif self.is_aiming:
            self.moving = False

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
        if self.is_aiming:
            self.current_frame = min(2, len(self.animations[self.direction]) - 1)
            return
        if self.is_dashing:
            self.current_frame = 0
            return
        if not self.moving and self.direction == 'up':
            self.current_frame = 0
            return

        current_target_time = self.animation_speed
        if not self.moving and self.current_frame == 0:
            current_target_time = self.idle_delay
        self.animation_timer += 1
        if self.animation_timer >= current_target_time:
            self.animation_timer -= current_target_time
            
            if self.moving:
                current_anim_length = len(self.animations[self.direction])
            else:
                current_anim_length = len(self.animations[f'idle_{self.direction}'])
                
            self.current_frame = (self.current_frame + 1) % current_anim_length

    def set_position(self, x, y):
        self.rect.center = (x, y)
        self.hitbox = self.rect.inflate(-12, -self.rect.height / 2)
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
                if prop.type == "door": 
                    dist = math.hypot(self.rect.centerx - prop.rect.centerx, self.rect.centery - prop.rect.centery)
                    if dist < 180:
                        if "key" in self.inventory:
                            self.inventory.remove("key")
                            return "next_level"
        return None
    
    def check_pits(self, pit_rects):
        for pit in pit_rects:
            if pit.collidepoint(self.hitbox.center):
                return "fall"
        return None