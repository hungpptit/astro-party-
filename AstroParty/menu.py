# File Menu.py

from Menu1 import Menu1
from Menu2 import Menu2
from Menu3 import Menu3
from background import Background

class Menu:
    def __init__(self, display_surface, game_instance, all_sprites):
        self.all_sprites = all_sprites
        self.display_surface = display_surface
        self.menu1 = Menu1(self.display_surface)
        self.menu2 = Menu2(self.display_surface)
        self.menu3 = Menu3(self.display_surface, self.all_sprites)
        self.background = Background(self.display_surface)
        self.game = game_instance  # Tham chiếu đến đối tượng Game

        # màn hình menu 
        self.state = 'menu1'

        # màn hình menu 2
        self.state_menu2 = False
        self.state_menu3 = False
        self.state_main_play = False

    def main_menu1(self):
        self.menu1.play_music()
        self.background.draw_backgound()
        self.menu1.draw_menu1()
    
    def main_menu2(self):
        if self.menu1.music_playing:
            self.menu1.menu_music.stop()
            self.menu1.music_playing = True
        if not self.menu2.music_menu2_playing:
            self.menu2.play_music()
        self.background.draw_backgound()
        
        start_pressed, exit_pressed = self.menu2.draw_menu2_1()
        # return start_pressed, exit_pressed
        
        

        if start_pressed:
            self.state = 'menu3'
            self.state_menu2 = False
            self.state_menu3 = True
        if exit_pressed:
            self.game.running = False
    
    def main_menu_3(self):
        self.background.draw_backgound()
        result = self.menu3.draw_menu()

        if result == 'back':
            self.state = 'back'
            self.state_menu2 = True
            self.state_menu3 = False
        elif result == 'next':
            self.state = 'playing'
            self.state_menu3 = False
            self.state_main_play = True
            self.menu2.music_menu2_playing = False
            self.menu2.menu2_music.stop()
            self.menu3.install_player()


 