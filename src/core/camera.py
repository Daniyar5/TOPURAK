class Camera:
    def __init__(self, width, height, lerp_speed=0.1):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.lerp_speed = lerp_speed 

    def update(self, player):
        target_x = player.rect.centerx - self.width / 2
        target_y = player.rect.centery - self.height / 2
        
        self.x += (target_x - self.x) * self.lerp_speed
        self.y += (target_y - self.y) * self.lerp_speed