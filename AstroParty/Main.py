from config import *
import buttons
from menu import *
from background import *
from gameplay import *
class Game:
    def __init__(self):
         # Initialize Pygame và hệ thống âm thanh
        pygame.init()  # Khởi tạo Pygame
        pygame.mixer.init()  # Khởi tạo hệ thống âm thanh
        # Setup
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.DOUBLEBUF)

        pygame.display.set_caption('Astro Party')
        icon = pygame.image.load(join('..', 'AstroParty','lesson1','assets', '11.png')).convert_alpha()
        
        pygame.display.set_icon(icon)
        self.running = True

        self.gameplay = Playgame(self.display_surface)   

        self.menu1 = Menu1(self.display_surface)
        self.menu2 = Menu2(self.display_surface)
        self.menu3 = Menu3(self.display_surface, self.gameplay.players_group)
        self.background = Background(self.display_surface)

        self.menu = Menu(self.display_surface, self, self.gameplay.players_group)


# hình như màn hình bị lệch 
    def run(self):
        while self.running:
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.menu.state == 'menu1':
                        self.menu.state = 'menu2'
                        self.menu.state_menu2 = True
                    if self.menu.state == "playing" and self.menu.state_main_play == True :    
                        if event.key == pygame.K_ESCAPE:
                            self.menu.state = 'menu3'
                            self.menu.state_menu3 = True
                            self.menu.state_main_play = False
                            if not self.menu.menu2.music_menu2_playing: # nếu nhạc chưa bật
                                self.menu.menu2.menu2_music.play(-1) # thêm tham số -1 để lặp lại nhạc
                                self.menu.menu2.music_menu2_playing = True
            if self.menu.state == "menu1": # Tắt menu 2
                self.menu.main_menu1()
            elif self.menu.state =='menu2' and self.menu.state_menu2 == True:
                self.menu.main_menu2()
            elif self.menu.state == 'menu3' and self.menu.state_menu3 == True:
                self.menu.main_menu_3()               
            elif self.menu.state == 'back':
                self.menu.main_menu2()
            elif self.menu.state == "playing" and self.menu.state_main_play == True :
                self.gameplay.main_play()  # Bắt đầu màn chơi chính

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()