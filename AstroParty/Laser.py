import pygame.transform

from config import *

class Lazer(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, player_id):
        super().__init__()
        # surf = pygame.Surface((33, 40))
        # surf1 = pygame.image.load('./image/lazer.png').convert_alpha()
        # self.image = pygame.transform.scale(surf1, (int(surf.get_width() * 3), int(surf.get_height() * 30)))
        self.player_id = player_id
        # self.original_image = pygame.transform.scale(surf1, (int(surf.get_width() * 3), int(surf.get_height() * 30)))
        self.image = pygame.image.load('./image/lazer.png').convert_alpha()
        self.original_image = pygame.image.load('./image/lazer.png').convert_alpha()
        self.width = self.image.get_width()  # Lấy chiều rộng của ảnh
        self.height = self.image.get_height()  # Lấy chiều cao của ảnh
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vantoc = 1  # Tốc độ di chuyển của laser
        self.theta = theta  # Góc quay của laser

        # Tính toán vị trí mới dựa trên góc theta
        lazer_x = self.x + self.height / 2.1 * (math.sin(self.theta - math.pi / 2) * self.vantoc)
        lazer_y = self.y + self.height / 2.1 * (math.cos(self.theta - math.pi / 2) * self.vantoc)

        # Cập nhật vị trí của rect
        self.image = pygame.transform.rotozoom(self.original_image, math.degrees(self.theta - math.pi / 2), 1)
        self.rect = self.image.get_rect(center=(lazer_x, lazer_y))

        # Thời gian sống của laser (milliseconds)
        self.lifetime = 100  # 0.5 giây
        self.creation_time = pygame.time.get_ticks()  # Thời gian tạo
        self.done = False

    def update(self, dt, players_group, rocks_group, dragonflies_group, bullets_group, swords_group, explosions_group):
        # Kiểm tra xem thời gian sống của laser đã hết chưa
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.done = True
            self.kill()  # Xóa laser nếu hết thời gian sống
        self.check_collision_with_player(players_group, explosions_group)
        self.check_collision_with_dragonfly(dragonflies_group, explosions_group)
        self.check_collision_with_rock(rocks_group, explosions_group)
        self.check_collision_with_bullet(bullets_group)
        self.check_collision_with_sword(swords_group)

    def check_collision_with_player(self, players_group, explosions_group):
        collided_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collided_player:
            for player in collided_player:
                if player.player_id != self.player_id: 
                    player.can_sword = False
                    player.kill_player(explosions_group)

    def check_collision_with_rock(self, rocks_group, explorsions_group):
        collided_rock = pygame.sprite.spritecollide(self, rocks_group, False, pygame.sprite.collide_mask)
        if collided_rock:
            rock = collided_rock[0]
            rock.kill_rock(explorsions_group)
    
    def check_collision_with_dragonfly(self, dragonflies_group, explorsions_group):
        collided_dragonfly = pygame.sprite.spritecollide(self, dragonflies_group, False, pygame.sprite.collide_mask)
        if collided_dragonfly:
            dragonfly = collided_dragonfly[0]
            dragonfly.kill_dragonfly(explorsions_group)

    def check_collision_with_bullet(self, bullets_group):
        collided_bullet = pygame.sprite.spritecollide(self, bullets_group, False, pygame.sprite.collide_mask)
        if collided_bullet:
            bullet = collided_bullet[0]
            bullet.kill()

    def check_collision_with_sword(self, swords_group):
        collided_sword = pygame.sprite.spritecollide(self, swords_group, False, pygame.sprite.collide_mask)
        if collided_sword:
            sword = collided_sword[0]
            sword.kill()
    
