from src.core.window import window, width, height
from src.utils.assets import load_animation_frames
from src.ui.button import Button

class Loss:
    def __init__(self):
        self.animations = {
            'fall': load_animation_frames('assets/sprites/player/game_over/fall', 'player_fall')
        }

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 60 / 8
        self.direction = 'fall'
        self.is_finished = False
        self.respawn_button = Button('assets/sprites/buttons/respawn.png', width * 0.23, height * 0.90)

    def reset(self):
        self.current_frame = 0
        self.animation_timer = 0
        self.is_finished = False

    def animation(self):
        if not self.is_finished:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                if self.current_frame < len(self.animations[self.direction]) - 1:
                    self.current_frame += 1
                else:
                    self.is_finished = True
                    
    def draw(self, events):
        self.animation()
        current_image = self.animations[self.direction][self.current_frame]
        window.blit(current_image, (0, 0))
        if self.is_finished:
            self.respawn_button.draw()
            for event in events:
                if self.respawn_button.click(event):
                    return "respawn"
                    
        return None
    