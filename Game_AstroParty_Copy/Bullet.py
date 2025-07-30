from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups, display_surface):
        super().__init__(groups)
        self.image = pygame.image.load('./image/bullet/Bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=player.rect.center)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.player = player
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 0.7
        self.angle = 360 - player.angle
        self.frame_index = 0
        self.groups = groups
        self.shoot_time = 0

    def move(self, dt):
        self.angle %= 360  # Điều chỉnh góc trong khoảng 0-360

        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        self.velocity = direction * self.max_speed * dt

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.x += self.velocity.x * dt
        self.y -= self.velocity.y * dt
        self.rect.center = (self.x, self.y)

        # Kiểm tra nếu đạn ra ngoài màn hình
        if not (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT):
            self.kill()

    def update(self, dt, display_surface):
        # if self.frame_index < 3:
        #     self.frame_index += dt * 0.015
        #     self.animate_shoot_explosion(display_surface)
        self.move(dt)

    def animate_shoot_explosion(self, display_surface):
        if self.frame_index >= 2:
            return
        # Tải ảnh animation dựa vào frame hiện tại
        image_path = f"./image/bullet/explore_shoot-{int(self.frame_index) % 2 + 1}.png"
        self.explosion_image = pygame.image.load(image_path).convert_alpha()

        # Vẽ ảnh explosion tại vị trí của player
        explosion_rect = self.explosion_image.get_rect(center=self.player.rect.center)
        display_surface.blit(self.explosion_image, explosion_rect)
