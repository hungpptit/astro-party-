import pygame.transform

from config import *

class Lazer(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, groups):
        super().__init__(groups)
        surf = pygame.Surface((33, 40))
        surf1 = pygame.image.load('./image/lazer.png').convert_alpha()
        self.image = pygame.transform.scale(surf1, (int(surf.get_width() * 3), int(surf.get_height() * 30)))

        self.original_image = pygame.transform.scale(surf1, (int(surf.get_width() * 3), int(surf.get_height() * 30)))
        self.width = self.image.get_width()  # Lấy chiều rộng của ảnh
        self.height = self.image.get_height()  # Lấy chiều cao của ảnh
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vantoc = 1  # Tốc độ di chuyển của laser
        self.theta = theta  # Góc quay của laser

        # Tính toán vị trí mới dựa trên góc theta
        lazer_x = self.x + self.height / 2.2 * (math.sin(self.theta - math.pi / 2) * self.vantoc)
        lazer_y = self.y + self.height / 2.2 * (math.cos(self.theta - math.pi / 2) * self.vantoc)

        # Cập nhật vị trí của rect
        self.image = pygame.transform.rotozoom(self.original_image, math.degrees(self.theta - math.pi / 2), 1)
        self.rect = self.image.get_rect(center=(lazer_x, lazer_y))

        # Thời gian sống của laser (milliseconds)
        self.lifetime = 200  # 0.5 giây
        self.creation_time = pygame.time.get_ticks()  # Thời gian tạo
        self.done = False

    def update(self, dt):
        # Kiểm tra xem thời gian sống của laser đã hết chưa
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.done = True
            self.kill()  # Xóa laser nếu hết thời gian sống
