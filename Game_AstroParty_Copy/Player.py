from config import *
from Bullet import *
from Laser import *
from Sword import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.images = [
            pygame.image.load("./image/blue_player/1.png").convert_alpha(),
            pygame.image.load("./image/blue_player/2.png").convert_alpha(),
            pygame.image.load("./image/blue_player/3.png").convert_alpha()
        ]
        self.image = self.images[0]
        self.frame_index = 0
        self.rect = self.image.get_rect(center=(400, 200)) #rect quản lý vị trí của hình ảnh
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 270  # Góc ban đầu của tàu
        self.max_speed = 0.25  # Tốc độ tối đa của tàu
        self.friction = 0.0001  # Ma sát
        self.rotation_speed = 0.3  # Tốc độ quay
        self.rot = False  # Kiểm tra có quay hay không
        self.T = 0
        self.shoot_time = 0
        self.shoot_laser_time = 0
        self.slash = False
        self.sl_time = 0
        self.can_shoot_laser = False
        self.can_sword = True
        self.swords = []

    def rotation(self, direction, dt):
        self.rot = True
        # direction = 1 (quay phải), -1 (quay trái)
        self.angle += self.rotation_speed * direction * dt
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

    def move(self, dt):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        acceleration = 0.0027 if self.rot else 0.002

        self.velocity += direction * self.max_speed * acceleration * dt
        self.velocity *= (1 - self.friction) if self.rot else 1

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if not self.rot:
            self.x += self.velocity.x * dt
            self.y += self.velocity.y * dt
        else:
            self.x += self.velocity.x / 1.7 * dt
            self.y += self.velocity.y / 1.7 * dt

        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH

        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

        self.rect.center = (self.x, self.y)

    def slash_move(self, dt):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))
        acceleration = 0.002
        self.velocity += direction * self.max_speed * acceleration * dt * 5

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        self.rect.center = (self.x, self.y)

    def update(self, dt, bullets_group, laser_group, sword_group, display_surface):
        self.frame_index += 3 * dt * 0.007
        self.load_image(dt)
        self.move(dt)
        self.handle_input(bullets_group, laser_group, display_surface, dt)
        self.rotate_sword(sword_group)

    def shoot(self, bullets_group, display_surface, dt):
        if self.shoot_time <= 0:
            self.shoot_time = 150
            bullet = Bullet(self, bullets_group, display_surface)
            bullets_group.add(bullet)
            radians = math.radians(self.angle)
            self.x -= 10 * math.cos(radians)
            self.y -= 10 * math.sin(radians)

    def shoot_laser(self, laser_group, dt):
        laser = Lazer(self.x, self.y, (math.radians(self.angle) - math.pi) * -1, laser_group)
        laser.add(laser_group)
        radians = math.radians(self.angle)
        self.x -= 30 * math.cos(radians)
        self.y -= 30 * math.sin(radians)
        self.max_speed = 0

    def rotate_sword(self, sword_group):
        if len(self.swords) < 3:
            self.swords.append(Sword(self, 0, sword_group))
            self.swords.append(Sword(self, 120, sword_group))
            self.swords.append(Sword(self, 240, sword_group))
        self.can_sword = False

    def handle_input(self, bullets_group, laser_group, display_surface, dt):
        if self.slash:
            self.slash_move(dt)
        self.sl_time -= 1
        if self.sl_time <= 0:
            self.slash = False
            self.sl_time = 0

        if pygame.mouse.get_pressed()[0] and not self.slash:
            self.rotation(1, dt)
            self.T = 3

        self.T -=  1
        if self.T <= 0: self.rot = False

        if pygame.mouse.get_pressed()[2]:
            if not self.can_shoot_laser:
                self.shoot(bullets_group, display_surface, dt)
            self.shoot_time -= 1
            if self.can_shoot_laser:
                self.shoot_time = 150
                self.shoot_laser(laser_group, dt)
                self.shoot_laser_time = 10
                self.can_shoot_laser = False

        self.shoot_laser_time -= 1
        if self.shoot_laser_time <= 0:
            self.shoot_laser_time = 0
            self.max_speed = 0.25



    def check_collision_with_rock(self):
        collided_wall = pygame.sprite.spritecollide(self, rocks, False, pygame.sprite.collide_mask)

    def check_collision_with_dragonfly(self):
        collied_dragonfly = pygame.sprite.spritecollide(self, dragonflies, True, pygame.sprite.collide_mask)
        if collied_dragonfly:
            self.kill()

    def load_image(self, dt):
        self.frame_index = (self.frame_index + dt * 3) % 3
        self.image = self.images[int(self.frame_index)]
        self.image = pygame.transform.rotozoom(self.image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
