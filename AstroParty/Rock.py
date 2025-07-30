from config import *
from explosion import *

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./image/big_rock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1300
        self.rect.y = random.randint(0, 720)
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = 180
        self.rot_agn = 0
        self.friction = 0
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 0.3
        
    def move(self, dt):
        #self.angle = 180
        direction = pygame.Vector2(math.cos(math.radians(self.angle)),
                                   math.sin(math.radians(self.angle)))

        self.velocity = direction * self.max_speed * dt

        self.x += self.velocity.x
        self.y -= self.velocity.y

        if 0 >= self.x:
            self.kill()

        self.rect.center = (self.x, self.y)

    def kill_rock(self, explosions_group):
        ''' Hàm này vừa cho nổ Rock khi va chạm vừa kill() nó trò chơi '''

        explosion = Explosion(self.rect.center)
        explosion.frames = [
            pygame.image.load(f"./image/explosion/rock/{i}.png").convert_alpha()
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
            self.kill_rock(explosions_group)

    def update(self, dt, players_group, explosions_group):
        self.move(dt)
        self.check_collision_with_player(players_group, explosions_group)
    