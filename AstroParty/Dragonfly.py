from config import *
from explosion import *

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
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
        self.player = None

    def load_image(self, dt):
        self.frame_index = (self.frame_index + dt * 3) % 1
        self.image = self.images[int(self.frame_index)]
        self.image = pygame.transform.rotozoom(self.image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def find_nearest_player(self, players_group):
        min_distance = float('inf')
        closest_player = None

        # Tìm player gần nhất trong players_groups
        for player in players_group:
            # Tính khoảng cách giữa self và player
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                (player.rect.centery - self.rect.centery) ** 2)
            
            # Nếu khoảng cách hiện tại nhỏ hơn khoảng cách ngắn nhất, cập nhật giá trị
            if distance < min_distance:
                min_distance = distance
                closest_player = player
        return closest_player

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

    def kill_dragonfly(self, explosions_group):
        ''' Hàm này vừa cho nổ Dragonfly khi va chạm vừa kill() nó trò chơi '''

        explosion = Explosion(self.rect.center)
        explosion.frames = [
            pygame.image.load(f"./image/explosion/dragonfly/{i}.png").convert_alpha()
            for i in range(1, 8)
        ]
        explosions_group.add(explosion)
        self.kill()

    def check_collision_with_player(self, players_group, explosions_group):
        collided_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collided_player:
            player = collided_player[0]
            player.can_sword = False
            player.kill_player(explosions_group)
            self.kill()

    def update(self, dt, players_group, explosions_group):
        #Tính khoảng cách của player gần nhất trong đối với vị trí hiện lại của self (player thuộc players_group)
        if self.find_nearest_player(players_group):
            self.player = self.find_nearest_player(players_group)
            self.move(self.player.rect.center[0], self.player.rect.center[1], dt)
            self.check_collision_with_player(players_group, explosions_group)
            self.load_image(dt)