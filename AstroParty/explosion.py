from config import *
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.frames = [pygame.image.load(f"./image/explosion/red_player/{i}.png").convert_alpha() for i in range(1, 8)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 0.07

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.kill()  # Kết thúc hiệu ứng nổ
        else:
            self.image = self.frames[int(self.current_frame)]