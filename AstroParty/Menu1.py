from config import *
from background import *

class Menu1():
    def __init__(self, display_surface):
        self.display_surface = display_surface
              
        self.menu_music = pygame.mixer.Sound(join('..', 'AstroParty', 'lesson1', 'sound', 'menu1.wav'))      
        
        self.direction = 1
        self.music_playing = False
        # self.text_menu = font_titles.render("Astro Party", True, (255, 165, 0))
        self.text_menu = font_titles.render("Astro Party", True, (255, 165, 0))
        self.logo_menu1 = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', '14_5.png')).convert_alpha()
        self.logo_menu1 = pygame.transform.scale2x(self.logo_menu1)
        

    def play_music(self):
        if not self.music_playing:
            self.menu_music.play(-1)
            self.music_playing = True
    def draw_menu1(self):
        # Hiển thị logo và tiêu đề
        self.display_surface.blit(self.text_menu, (430, 100))
        self.display_surface.blit(self.logo_menu1, (490, 200))
        
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            text = font_start.render("Press 'SPACE' to Start", True, (255, 255, 0))
            self.display_surface.blit(text, (470, 600))

