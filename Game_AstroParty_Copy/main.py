import pygame
from Player import *
from Bullet import *
from Dragonfly import *
from Rock import *
from Port import *
from Skill import *
from Laser import *
from config import *
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        #Khởi tạo các nhóm đối tượng trong trò chơi
        self.players_group = pygame.sprite.Group()
        self.player = Player(self.players_group)
        self.players_group.add(self.player)

        self.bullets_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.sword_group = pygame.sprite.Group()

        self.ports_group = pygame.sprite.Group()

        self.dragonfies_group = pygame.sprite.Group()

        self.skills_group = pygame.sprite.Group()
        self.skill_spawn_time = 0
        self.skill_spawn_interval = 10000

        #Khởi tạo các biến quản lý thời gian
        self.rocks_group = pygame.sprite.Group()
        self.rock_spawn_time = 0
        self.rock_spawn_interval = 1000

        self.dbclock = pygame.time.Clock()

        # self.port_spawn_time = pygame.time.get_ticks()  # Thời gian spawn Port
        self.port_spawn_time = 0
        self.port_spawn_interval = 5000
        self.port_duration = 2000  # Port tồn tại trong 2 giây

    def run(self):
        T = 0
        dem = 0
        DOUBLECLICKTIME = 250
        kt_rock = False
        while self.running:
            self.screen.fill('black')
            dt = self.clock.tick(1000)

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dbclock.tick() < DOUBLECLICKTIME and pygame.mouse.get_pressed()[0]:
                        self.player.slash = True
                        self.player.sl_time = 200

                    else:
                        self.player.slash = False

            # Spawn rock every 20 seconds
            current_time = pygame.time.get_ticks()
            if not current_time % 15000: kt_rock = True
            if kt_rock:
                if current_time - self.rock_spawn_time > self.rock_spawn_interval:
                    self.rock = Rock(self.rocks_group)
                    self.rocks_group.add(self.rock)
                    self.rock_spawn_time = current_time
                    dem += 1
            if dem == 5:
                kt_rock = False
                dem = 0

            if current_time - self.port_spawn_time > self.port_spawn_interval:
                self.port = Port(self.ports_group)
                self.ports_group.add(self.port)
                self.port_spawn_time = current_time

            #Appear dragonfly
            if current_time - self.port_spawn_time > self.port_duration and len(self.dragonfies_group) < 4:
                # Remove the Port
                if self.ports_group:
                    dragonfly = Dragonfly(self.dragonfies_group, self.port.rect.center[0], self.port.rect.center[1])
                    self.dragonfies_group.add(dragonfly)
                self.ports_group.empty()

            #Appear skill
            if current_time - self.skill_spawn_time > self.port_spawn_interval:
                self.skill = Skill(self.skills_group)
                self.skills_group.add(self.skill)
                self.skill_spawn_time = current_time



            #update
            self.rocks_group.update(dt, self.rocks_group, self.players_group, self.bullets_group)
            self.players_group.update(dt, self.bullets_group, self.laser_group, self.sword_group, self.screen)
            self.bullets_group.update(dt, self.screen)
            self.laser_group.update(dt)
            self.dragonfies_group.update(self.player, dt, self.bullets_group)
            self.ports_group.update(dt)
            self.skills_group.update(dt, self.players_group)
            self.sword_group.update(self.screen, dt)

            #draw
            self.laser_group.draw(self.screen)
            self.rocks_group.draw(self.screen)
            self.players_group.draw(self.screen)
            self.bullets_group.draw(self.screen)
            self.dragonfies_group.draw(self.screen)
            self.ports_group.draw(self.screen)
            self.skills_group.draw(self.screen)
            self.sword_group.draw(self.screen)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()