import pygame.sprite

from config import *
class Port(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.images = [pygame.image.load(f"./image/port/{i}.png").convert_alpha() for i in range(1, 27)]
        self.image = self.images[0]
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 550)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.frame_index = 0

    def load_image(self, dt):
        if self.frame_index < 25:
            self.frame_index = (self.frame_index + dt *0.02)
            self.image = self.images[int(self.frame_index)]
        elif self.frame_index < 50:
            self.frame_index = (self.frame_index + dt * 0.02)
            self.image = self.images[50-int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        if self.frame_index < 52: self.load_image(dt)