from config import *
import pygame
import buttons
from boom import *

class Background:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.bg = pygame.image.load(join('..', 'AstroParty','lesson1','assets', 'background_new.png')).convert_alpha()
        self.bg_menu_up = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'background.png')).convert_alpha()
        self.bg_menu_up_up = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'background2.png')).convert_alpha()
        self.map1 = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'map1.png')).convert_alpha()
        self.map2 = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'map2.png')).convert_alpha()

        self.bg_x = 0
        self.bg_menu_up_up_x = 0
        self.direction = 1

        self.shake_duration = 0  # Thời gian rung màn hình
        self.offset = (0,0)  # Offset cho rung màn hình
        
    def draw_backgound(self):
        self.display_surface.blit(self.bg, (0, 0))
        self.display_surface.blit(self.bg_menu_up, (0, 0))
        
        # Di chuyển hình nền
        self.bg_menu_up_up_x += 1 * (self.direction / 10)
        self.display_surface.blit(self.bg_menu_up_up, (self.bg_menu_up_up_x - 50, -15))
        if self.bg_menu_up_up_x >= 50:
            self.direction = -1
        elif self.bg_menu_up_up_x <= -50:
            self.direction = 1
    
    def set_shake_duration(self, duration):
        """Đặt thời gian rung màn hình."""
        self.shake_duration = duration 

    def draw_main_play(self, map_id):
        if self.shake_duration > 0:
            self.shake_duration -=5
            offset_x = random.randint(-20, 20) 
            offset_y = random.randint(-20, 20) 
            
            self.offset = (offset_x, offset_y)  # Gán giá trị offset mới
        else:
            self.offset = (0, 0)  # Hết thời gian rung

        if map_id == 0:
            self.display_surface.blit(self.bg, self.offset)
        if map_id == 1:
            self.display_surface.blit(self.map1, self.offset)
        if map_id == 2:
            self.display_surface.blit(self.map2, self.offset)
        
        
        return self.offset
   

