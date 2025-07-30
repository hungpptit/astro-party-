from config import * 

bomb_music = pygame.mixer.Sound(join('..', 'AstroParty','lesson1','sound', 'boom.mp3'))
bomb_music.set_volume(1)
bomb_channel = pygame.mixer.Channel(3) 
class Boom(pygame.sprite.Sprite):
    def __init__(self, player, groups, background):
        super().__init__(groups)
        self.image = pygame.image.load('./image/skill_bomb/boom.png').convert_alpha()
        self.copy_image = self.image
        self.rect = self.image.get_rect(center=(player.x, player.y))
        self.x = player.x
        self.y = player.y
        self.lifetime = 500  # Thời gian tồn tại của boom1
        self.start = pygame.time.get_ticks()  # Thời gian khởi tạo
        self.updated_image = False
        self.can_boom = False
        self.angle = 0
        self.rotation_start_time = None
        self.current_time = 0
        self.creation_time = None  # Thời gian bắt đầu hiển thị boom1
        self.player = player
        self.bang_bomb = False # Kiểm tra đã nổ hay chưa

        self.background = background

    def rotation(self):
        self.angle += 3
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

        self.image = pygame.transform.rotozoom(self.copy_image, -self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def bang(self, players_group, rocks_group, dragonflies_group, explosions_group):
        current_time = pygame.time.get_ticks()
        if self.rotation_start_time is None:
            self.rotation_start_time = current_time
        elapsed_time = current_time - self.rotation_start_time
        if elapsed_time < 600:
            self.rotation()
        elif elapsed_time >= 600 and not self.can_boom:  # Sau 1 giây quay, thực hiện boom
            self.can_boom = True
            self.creation_time = pygame.time.get_ticks()  # Ghi lại thời gian khi boom1 bắt đầu xuất hiện
            self.image = pygame.image.load('./image/skill_bomb/boom1.png').convert_alpha()
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.updated_image = True
            self.background.set_shake_duration(300)
            bomb_channel.play(bomb_music)
            
                
           
    def check_distance(self, players_group, rocks_group, dragonflies_group, explosions_group):
        for player in players_group:
           if player.player_id != self.player.player_id:
                distance = math.sqrt(
                    (player.rect.center[0] - self.rect.center[0]) ** 2 + (player.rect.center[1] - self.rect.center[1]) ** 2)
                if distance < 100:
                    self.bang_bomb = True
        if self.bang_bomb:
            self.bang(players_group, rocks_group, dragonflies_group, explosions_group)
            

    def update(self, players_group, rocks_group, dragonflies_group, bullets_group, laser_group, swords_group, explosions_group):
       #ktra có ai đến gần thì gọi hàm bang
        self.check_distance(players_group, rocks_group, dragonflies_group, explosions_group)
        if self.updated_image:
            self.current_time = pygame.time.get_ticks()
            self.check_collision_with_player(players_group, explosions_group)
            self.check_collision_with_dragonfly(dragonflies_group, explosions_group)
            self.check_collision_with_rock(rocks_group, explosions_group)
            if self.current_time - self.creation_time > self.lifetime:
                self.kill()

        self.check_collsion_with_bullet(bullets_group)
        self.check_collsion_with_laser(laser_group)
        self.check_collsion_with_sword(swords_group)
    def check_collision_with_player(self, players_group, explosions_group):
        collided_player = pygame.sprite.spritecollide(self, players_group, False, pygame.sprite.collide_mask)
        if collided_player:
            player = collided_player[0]
            player.can_sword = False
            player.kill_player(explosions_group)
    
    def check_collision_with_dragonfly(self, dragonflies_group, explorsions_group):
        collided_dragonfly = pygame.sprite.spritecollide(self, dragonflies_group, False, pygame.sprite.collide_mask)
        if collided_dragonfly:
            dragonfly = collided_dragonfly[0]
            dragonfly.kill_dragonfly(explorsions_group)

    def check_collision_with_rock(self, rocks_group, explorsions_group):
        collided_rock = pygame.sprite.spritecollide(self, rocks_group, False, pygame.sprite.collide_mask)
        if collided_rock:
            rock = collided_rock[0]
            rock.kill_rock(explorsions_group)
    
    def check_collsion_with_bullet(self, bullets_group):
        collided_bullet = pygame.sprite.spritecollide(self, bullets_group, False, pygame.sprite.collide_mask)
        if collided_bullet:
            bullet = collided_bullet[0]
            bullet.kill()
            self.bang_bomb = True

    def check_collsion_with_laser(self, laser_group):
        collided_laser = pygame.sprite.spritecollide(self, laser_group, False, pygame.sprite.collide_mask)
        if collided_laser:
            self.bang_bomb = True
    def check_collsion_with_sword(self, swords_group):
        collided_sword = pygame.sprite.spritecollide(self, swords_group, False, pygame.sprite.collide_mask)
        if collided_sword:
            sword = collided_sword[0]
            sword.kill()
            self.bang_bomb = True