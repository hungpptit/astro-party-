from config import *
import buttons


class Menu2:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.menu2_music = pygame.mixer.Sound(join('..', 'AstroParty', 'lesson1', 'sound', 'music_menu2+.mp3'))
        self.music_menu2_playing = False

        self.logo_menu2 = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'logo.png')).convert_alpha()
        self.logo_menu2 = pygame.transform.scale2x(self.logo_menu2)
        self.start_button = buttons.Button(316, 530, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'start_btn1.png')).convert_alpha())
        self.exit_button = buttons.Button(824, 530, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'exit_btn1.png')).convert_alpha())



        

    def play_music(self):
        if not self.music_menu2_playing:
            self.menu2_music.play(-1)  # Phát lặp nhạc
            self.music_menu2_playing = True

    def stop_music(self):
        if self.music_menu2_playing:
            self.menu2_music.stop()
            self.music_menu2_playing = False
    def draw_menu2_1(self):
        self.display_surface.blit(self.logo_menu2, (316, 200))
        start_pressed = self.start_button.draw(self.display_surface)
        exit_pressed = self.exit_button.draw(self.display_surface)

        return start_pressed, exit_pressed
    
    
    
        