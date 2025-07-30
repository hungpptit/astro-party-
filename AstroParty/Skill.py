import math

from config import *

class Skill(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.skill_num = random.randint(1, 4)
        if self.skill_num == 1:
            self.images = self.images = [pygame.image.load(f"./image/skill_laser/{i}.png").convert_alpha() for i in range(1, 8)]
        if self.skill_num == 2:
            self.images = self.images = [pygame.image.load(f"./image/skill_sword/{i}.png").convert_alpha() for i in range(1, 8)]
        if self.skill_num == 3:
            self.images = self.images = [pygame.image.load(f"./image/skill_bomb/{i}.png").convert_alpha() for i in range(1, 8)]
        if self.skill_num == 4:
            self.images = self.images = [pygame.image.load(f"./image/skill_reverse/{i}.png").convert_alpha() for i in range(1, 8)]

        self.image = self.images[0]
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 550)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.frame_index = 0
        self.rotation_speed = 0.05
        self.angle = 0
        self.max_speed = 1
        self.velocity = pygame.Vector2(0, 0)

    def rotation(self, dt):
        self.angle += self.rotation_speed * dt
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

    def draw_circle(self, screen):
        # Vẽ hình tròn lên màn hình
        screen.blit(self.circle_surface, self.circle_rect.topleft)
    def load_image(self, dt):
        self.frame_index = (self.frame_index + dt * 0.01) % 7
        self.image = self.images[int(self.frame_index)]
        self.image = pygame.transform.rotozoom(self.image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    def check_collision_with_player(self, dt, players_group):
        for player in players_group:
            distance = math.sqrt((player.rect.center[0] - self.rect.center[0])**2 + (player.rect.center[1] - self.rect.center[1])**2)
            if distance < 100:
                radians = math.atan2(player.rect.center[1] - self.rect.center[1], player.rect.center[0] - self.rect.center[0])
                direction = pygame.Vector2(math.cos(radians), math.sin(radians))

                self.velocity += direction * self.max_speed * 0.001 * dt

                if self.velocity.length() > self.max_speed:
                    self.velocity = self.velocity.normalize() * self.max_speed

                self.x += self.velocity.x * dt
                self.y += self.velocity.y * dt

                self.rect.center = (self.x, self.y)

        collied_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collied_player:
            player = collied_player[0]
            if self.skill_num == 1:
                player.can_shoot_laser = True
                player.can_sword = False
                player.can_place_bomb = False
            if self.skill_num == 2:
                player.can_shoot_laser = False
                player.can_sword = True
                player.can_place_bomb = False
            if self.skill_num == 3:
                player.can_shoot_laser = False
                player.can_sword = False
                player.can_place_bomb = True
            if self.skill_num == 4:
                for player in players_group:
                    player.direction *= -1

            self.kill()

    def update(self, dt, players_group):
        self.rotation(dt)
        self.load_image(dt)
        self.check_collision_with_player(dt, players_group)
