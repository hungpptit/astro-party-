from config import *
from Bullet import *
from Laser import *
from Sword import *
from boom import *

fire_music = pygame.mixer.Sound(join('..', 'AstroParty','lesson1','sound', 'laser-gun.mp3'))
fire_music.set_volume(1)
laser_music = pygame.mixer.Sound(join('..', 'AstroParty','lesson1','sound', 'laser.mp3'))
laser_music.set_volume(1)
laser_channel = pygame.mixer.Channel(1)  # Kênh 1 cho âm thanh laser
fire_channel = pygame.mixer.Channel(2)   # Kênh 2 cho âm thanh fire

class Player(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.player_id = id
        if self.player_id == 1:
            self.images = [
                pygame.image.load("./image/blue_player/1.png").convert_alpha(),
                pygame.image.load("./image/blue_player/2.png").convert_alpha(),
                pygame.image.load("./image/blue_player/3.png").convert_alpha()
            ]
            self.image = self.images[0]
            self.rect = self.image.get_rect(center=(60, 60))
            self.key = [pygame.K_1, pygame.K_2]
            self.angle = 45  # Góc ban đầu của tàu

        if self.player_id == 2:
            self.images = [
                pygame.image.load("./image/red_player/1.png").convert_alpha(),
                pygame.image.load("./image/red_player/2.png").convert_alpha(),
                pygame.image.load("./image/red_player/3.png").convert_alpha()
            ]
            self.image = self.images[0]
            self.rect = self.image.get_rect(center=(1200, 670))
            self.key = [pygame.K_v, pygame.K_b]
            self.angle = 225  # Góc ban đầu của tàu

        if self.player_id == 3:
            self.images = [
                pygame.image.load("./image/green_player/1.png").convert_alpha(),
                pygame.image.load("./image/green_player/2.png").convert_alpha(),
                pygame.image.load("./image/green_player/3.png").convert_alpha()
            ]
            self.image = self.images[0]
            self.rect = self.image.get_rect(center=(1200, 60))
            self.key = [pygame.K_LEFT, pygame.K_RIGHT]
            self.angle = 135  # Góc ban đầu của tàu

        if self.player_id == 4:
            self.images = [
                pygame.image.load("./image/purple_player/1.png").convert_alpha(),
                pygame.image.load("./image/purple_player/2.png").convert_alpha(),
                pygame.image.load("./image/purple_player/3.png").convert_alpha()
            ]
            self.image = self.images[0]
            self.rect = self.image.get_rect(center=(60, 670))
            self.key = [pygame.K_KP_8, pygame.K_KP_9]
            self.angle = 315  # Góc ban đầu của tàu

        self.frame_index = 0 #Biến quản lý chuyển động ảnh của Player

        self.stop = True

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        #Biến dùng cho di chuyển
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 0.3  # Tốc độ tối đa của tàu
        self.friction = 0.0001  # Ma sát
        self.rotation_speed = 0.3  # Tốc độ quay
        self.rot = False  # Kiểm tra có quay hay không
        self.T = 0
        self.direction = 1

        self.is_shooting = False

        #Biến dùng cho bắn
        self.shoot_time = 0
        self.ball_count = 2  # Initial number of available balls
        self.max_balls = 2 # Maximum number of balls
        self.ball_recharge_time = 700  # Time in ms to recharge one ball
        self.last_recharge_time = 0

        #Biến dùng cho skill laser
        self.shoot_laser_time = 0
        self.can_shoot_laser = False

        #Biến dùng cho flash
        self.flash_time_long = 0
        self.flash = False
        self.was_key0_pressed = False
        self.flash_cooldown = 1000
        self.last_flash_time = 0
        self.last_release_time = None
        self.last_press_time = None

        #Các biến dùng cho skill kiếm
        self.can_sword = False
        self.swords = []

        #Biến dùng cho skill bomb
        self.can_place_bomb = False


    def load_image(self, dt):
        self.frame_index = (self.frame_index + dt * 3) % 3
        self.image = self.images[int(self.frame_index)]
        self.image = pygame.transform.rotozoom(self.image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate(self, dt):
        """Dùng để xoay may bay"""
        self.rot = True
        # direction = 1 (quay theo chiều kim đồng hồ), -1 (chiều ngược lại)
        self.angle += self.rotation_speed * self.direction * dt
        # Đảm bảo góc nằm trong đoạn [0,360] để dễ quản lý
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

    def move(self, dt):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        acceleration = 0.0027 if self.rot else 0.002

        self.velocity += direction * self.max_speed * acceleration * dt
        #velocity = velocity + direction * self.max_speed * acceleration * dt

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

    def flash_move(self, dt):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))
        acceleration = 0.002
        self.velocity += direction * self.max_speed * acceleration * dt * 5

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        self.rect.center = (self.x, self.y)

    def shoot(self, bullets_group):
        if self.shoot_time <= 0:
            self.shoot_time = 1
            self.fire_bullet(bullets_group)
            radians = math.radians(self.angle)
            self.x -= 10 * math.cos(radians)
            self.y -= 10 * math.sin(radians)
            fire_channel.play( fire_music)

    def fire_bullet(self, bullets_group):
        if self.ball_count > 0:  # Chỉ bắn khi còn đạn
            bullet = Bullet(self)
            bullets_group.add(bullet)  # Tạo đạn mới
            self.ball_count -= 1  # Giảm số đạn đi 1
            if self.ball_count == 0:  # Nếu hết đạn, bắt đầu bộ đếm thời gian hồi đạn
                self.last_recharge_time = pygame.time.get_ticks()

    def recharge_balls(self):
        current_time = pygame.time.get_ticks()
        if self.ball_count < self.max_balls:
            # Kiểm tra nếu đủ thời gian hồi đạn đã trôi qua
            if current_time - self.last_recharge_time >= self.ball_recharge_time:
                self.ball_count += 1  # Hồi lại 1 viên đạn
                self.last_recharge_time = current_time  # Cập nhật thời gian hồi đạn

    def shoot_laser(self, laser_group):
        laser = Lazer(self.x, self.y, (math.radians(self.angle) - math.pi) * -1, self.player_id)
        laser.add(laser_group)
        radians = math.radians(self.angle)
        self.x -= 20 * math.cos(radians)
        self.y -= 20 * math.sin(radians)
        self.max_speed = 0
        laser_channel.play(laser_music)

    def rotate_sword(self, sword_group):
        if len(self.swords) < 3:
            sword1 = Sword(self, 0)
            sword_group.add(sword1)
            sword2 = Sword(self, 120)
            sword_group.add(sword2)
            sword3 = Sword(self, 240)
            sword_group.add(sword3)
            self.swords.append(sword1)
            self.swords.append(sword2)
            self.swords.append(sword3)
        self.can_sword = False

    def place_bomb(self, bomb_group, background):
        bomb = Boom(self, bomb_group, background)
        bomb.add(bomb_group)

    def handle_input(self, bullets_group, laser_group, bomb_group, sword_group, dt, background):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[self.key[0]]:
            if (self.last_release_time and (current_time - self.last_release_time < 300)
                    and (current_time - self.last_flash_time > self.flash_cooldown)):
                self.flash = True
                self.flash_time_long = 100
                self.last_release_time = None 
                self.last_flash_time = current_time

            elif not self.flash:
                self.rotate(dt)
                self.T = 10
                self.last_press_time = current_time
            
            self.was_key0_pressed = True

        elif not keys[self.key[0]] and self.was_key0_pressed:
            if self.last_press_time:
                self.last_release_time = current_time
                self.was_key0_pressed = False

        if self.flash:
            self.flash_move(dt)
            self.flash_time_long -= 1
        if self.flash_time_long <= 0:
            self.flash = False
            self.flash_time_long = 0

        if keys[self.key[1]]:
            if not self.is_shooting:  # Chỉ bắn khi chưa trong trạng thái bắn
                if self.can_shoot_laser:
                    self.shoot_time = 1
                    self.shoot_laser(laser_group)
                    background.set_shake_duration(300)
                    self.shoot_laser_time = 10
                    self.can_shoot_laser = False
                elif self.can_place_bomb:
                    self.shoot_time = 1
                    self.place_bomb(bomb_group, background)
                    self.can_place_bomb = False
                elif self.can_sword:
                    self.rotate_sword(sword_group)
                    self.can_sword = False
                else:
                    self.shoot(bullets_group)
                    
                    self.shoot_time -= 1
                self.is_shooting = True  # Đánh dấu đã bắn để không bắn liên tục
        else:
            self.is_shooting = False  # Đặt lại khi phím được nhả ra

        self.T -= 1
        if self.T <= 0:
            self.rot = False

        self.shoot_laser_time -= 1
        if self.shoot_laser_time <= 0:
            self.shoot_laser_time = 0
            self.max_speed = 0.3

    def kill_player(self, explosions_group):
        ''' Hàm này vừa cho nổ Rock khi va chạm vừa kill() nó trò chơi '''

        explosion = Explosion(self.rect.center)
        explosion.frames = [
            pygame.image.load(f"./image/explosion/rock/{i}.png").convert_alpha()
            for i in range(1, 8)
        ]
        explosions_group.add(explosion)
        self.kill()

    def update(self, dt, bullets_group, laser_group, sword_group, bomb_group, background):
        self.frame_index += 3 * dt * 0.007
        self.load_image(dt)
        if not self.stop:
            self.move(dt)
        self.handle_input(bullets_group, laser_group, bomb_group, sword_group, dt, background)
        self.recharge_balls()

    
