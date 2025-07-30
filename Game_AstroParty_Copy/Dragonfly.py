import pygame.sprite

from config import *

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, groups, x, y):
        super().__init__(groups)
        self.images = [pygame.image.load('./image/Dragonfly.png').convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.frame_index = 0
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = random.randint(0,360)
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 0.25
        self.rotation_speed = 0.25

    def find_nearest_player(self):
        pass

    def update(self, player, dt, bullets_group):
        # self.rotation(dt)
        self.move(player.rect.center[0], player.rect.center[1], dt)
        self.check_collision_bullet(bullets_group)
        self.load_image(dt)

    def rotation(self, dt):
        self.angle += self.rotation_speed * dt
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

    def move(self, p_x, p_y, dt):
        "chuồn chuồn sẽ đuổi theo player(p_x, p_y)"
        radians = math.atan2(p_y - self.y, p_x - self.x)
        self.angle = math.degrees(radians)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        self.velocity += direction * self.max_speed * 0.001 * dt

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH

        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT
        self.rect.center = (self.x, self.y)

    def check_collision_bullet(self, bullets_group):
        collied_bullet = pygame.sprite.spritecollide(self, bullets_group, True, pygame.sprite.collide_mask)
        if collied_bullet:
            self.kill()
            bullet = collied_bullet[0]
            bullet.kill()
            bullets_group.remove(bullet)

    def load_image(self, dt):
        self.frame_index = (self.frame_index + dt * 3) % 1
        self.image = self.images[int(self.frame_index)]
        self.image = pygame.transform.rotozoom(self.image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)