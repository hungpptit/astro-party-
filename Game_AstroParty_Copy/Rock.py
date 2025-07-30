from config import *

class Rock(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./image/big_rock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = random.randint(0, 720)
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = 180
        self.rot_agn = 0
        self.friction = 0
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0.3

    def update(self, dt, rocks_group, players_group, bullets_group):
        self.move(dt)
        self.check_collision_with_player(players_group)
        self.check_collision_with_bullet(bullets_group)
    def move(self, dt):
        self.angle %= 360  # Optimized angle normalization

        direction = pygame.Vector2(math.cos(math.radians(self.angle)),
                                   math.sin(math.radians(self.angle)))

        self.velocity = direction * self.speed * dt

        self.x += self.velocity.x
        self.y -= self.velocity.y

        if not (0 <= self.x and 0 <= self.y <= SCREEN_HEIGHT):
            self.kill()

        self.rect.center = (self.x, self.y)

    def check_collision_with_player(self, players_group):
        collided_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collided_player:
            player = collided_player[0]
            player.kill()
            self.kill()

    def check_collision_with_bullet(self, bullets_group):
        collided_bullet = pygame.sprite.spritecollide(self, bullets_group, True, pygame.sprite.collide_mask)
        if collided_bullet:
            bullet = collided_bullet[0]
            bullet.kill()
            self.kill()