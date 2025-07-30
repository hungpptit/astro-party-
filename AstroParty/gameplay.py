from config import *
from Player import *
from Bullet import *
from Skill import *
from Laser import *
from Rock import *
from Dragonfly import *
from Port import *
from config import *
from menu import *

class Playgame:
    def __init__(self, display_surface):
        self.display_surface = display_surface
#--------------------------------Groups------------------------------
        self.players_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()
        self.game_started = False
        self.wait_time = 1500
        
#--------------------------------Skill-------------------------------
        self.bullets_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.sword_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()

        self.skills_group = pygame.sprite.Group()
        self.skill_spawn_time = 0
        self.skill_spawn_interval = 7000

#--------------------------------Obstacle----------------------------
        #Port để xuất hiện quái vật
        self.ports_group = pygame.sprite.Group()
        self.port_spawn_time = 0
        self.port_spawn_interval = 10000
        self.port_duration = 2000  # Port tồn tại trong 2 giây

        #Dragonfly
        self.dragonflies_group = pygame.sprite.Group()

        #Rock
        self.rocks_group = pygame.sprite.Group()
        self.rock_spawn_time = 0
        self.rock_spawn_interval = 1000
        self.next_spawn_time = 0
        self.check_rock = False
        self.rock_count = 0

##--------------------------------Menu-------------------------------
        self.menu2 = Menu2(self.display_surface)
        self.menu3 = Menu3(self.display_surface, self.players_group)
        self.background = Background(self.display_surface)

        #Biến xử lý random map
        self.map_id = 0
        self.MAP_RANDOM_TIME = 15000
        self.map_last_random_time = 0


        self.menu = Menu(self.display_surface, self, self.players_group)
        self.clock = pygame.time.Clock()
    
    def spawn_rock(self, current_time):
        if current_time >= self.next_spawn_time:
            self.check_rock = True
            self.next_spawn_time += 10000
        
        if self.check_rock:
            if current_time - self.rock_spawn_time > self.rock_spawn_interval:
                rock = Rock()
                self.rocks_group.add(rock)
                self.rock_spawn_time = current_time
                self.rock_count += 1

        if self.rock_count == 5:
            self.check_rock = False
            self.rock_count = 0

    def spawn_port(self, current_time):
        if current_time - self.port_spawn_time > self.port_spawn_interval and len(self.dragonflies_group) <2:
            self.port = Port()
            self.ports_group.add(self.port)
            self.port_spawn_time = current_time

        if current_time - self.port_spawn_time > self.port_duration and len(self.dragonflies_group) < 2:
            # Xóa Port và thêm Dragonfly
            if self.ports_group:
                dragonfly = Dragonfly(self.port.rect.center[0], self.port.rect.center[1])
                self.dragonflies_group.add(dragonfly)
            self.ports_group.empty()

    
    def main_play(self):
        # delta time
        if not self.game_started:
            self.start_game_time = pygame.time.get_ticks()
            self.game_started = True

        dt = self.clock.tick(1000)
        if dt > 10: 
            dt = 2
        current_time = pygame.time.get_ticks()

        #Random map
        if current_time - self.map_last_random_time > self.MAP_RANDOM_TIME: #15s
            self.map_id = random.randint(0, 2)
            self.map_last_random_time = current_time

        self.offset = self.background.draw_main_play(self.map_id)    

        for player in self.players_group:
        # Tạo bản sao vị trí để tránh thay đổi tọa độ thực tế của nhân vật
            original_position = player.rect.topleft
            # Điều chỉnh vị trí để hiển thị rung
            player.rect.topleft = (original_position[0] + self.offset[0], original_position[1] + self.offset[1])
            self.display_surface.blit(player.image, player.rect)  # Vẽ nhân vật tại vị trí điều chỉnh    

        if self.map_id == 1:
            self.spawn_port(current_time) 
        if self.map_id == 2:
            self.next_spawn_time = current_time
            self.spawn_rock(current_time) 

        esc_key = pygame.key.get_pressed()
        if esc_key[pygame.K_ESCAPE]:
            self.menu.state = 'menu3'
            self.menu.state_menu3 = True
            self.menu.state_main_play = False
            if not self.menu2.music_menu2_playing: # nếu nhạc chưa bật
                self.menu2.menu2_music.play(-1) # thêm tham số -1 để lặp lại nhạc
                self.menu2.music_menu2_playing = True
        
        current_time = pygame.time.get_ticks()

        #Appear skill
        if current_time - self.skill_spawn_time > self.skill_spawn_interval:
            self.skill = Skill(self.skills_group)
            self.skills_group.add(self.skill)
            self.skill_spawn_time = current_time
    
        if current_time - self.start_game_time > self.wait_time:
            for player in self.players_group:
                player.stop = False
        #update
        self.rocks_group.update(dt, self.players_group, self.explosions_group)
        self.players_group.update(dt, self.bullets_group, self.laser_group, self.sword_group, self.bomb_group, self.background)
        self.skills_group.update(dt, self.players_group)
        self.bullets_group.update(dt, self.display_surface, self.players_group, self.rocks_group, self.dragonflies_group, self.explosions_group)
        self.laser_group.update(dt, self.players_group, self.rocks_group, self.dragonflies_group, self.bullets_group, self.sword_group, self.explosions_group)
        self.sword_group.update(dt, self.players_group, self.rocks_group, self.dragonflies_group, self.explosions_group)
        self.bomb_group.update(self.players_group, self.rocks_group, self.dragonflies_group, self.bullets_group, self.laser_group, self.sword_group, self.explosions_group)
        self.dragonflies_group.update(dt, self.players_group, self.explosions_group)
        self.ports_group.update(dt)
        self.explosions_group.update()

        #draw
        self.laser_group.draw(self.display_surface)
        self.rocks_group.draw(self.display_surface)
        self.players_group.draw(self.display_surface)
        self.bullets_group.draw(self.display_surface)
        self.skills_group.draw(self.display_surface)
        self.sword_group.draw(self.display_surface)
        self.dragonflies_group.draw(self.display_surface)
        self.ports_group.draw(self.display_surface)
        self.explosions_group.draw(self.display_surface)
        self.bomb_group.draw(self.display_surface)