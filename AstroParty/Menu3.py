from config import *
import buttons
from Player import *



class Menu3:
    def __init__(self, display_surface, players_group):
        self.display_surface = display_surface
        self.p1p = buttons.Button(320,300, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', '1p.png')).convert_alpha())
        self.p2p = buttons.Button(490,300, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', '2p.png')).convert_alpha())
        self.p3p = buttons.Button(660,300, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', '3p.png')).convert_alpha())
        self.p4p = buttons.Button(830,300, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', '4p.png')).convert_alpha())
        self.back = buttons.Button(10,10, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'back-1.png.png')).convert_alpha())
        self.next = buttons.Button(1187,10, pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'next.png')).convert_alpha())
        self.chose_img = pygame.image.load(join('..', 'AstroParty', 'lesson1', 'assets', 'chose1.png')).convert_alpha()

        self.p1p_selected = False
        self.p2p_selected = False
        self.p3p_selected = False
        self.p4p_selected = False
        self.number_player_1 = False
        self.number_player_2 = False
        self.number_player_3 = False
        self.number_player_4 = False
        self.players_group = players_group
    
    def clear_players(self, players_group):
        self.players_group.empty()  # Xóa tất cả sprite trong nhóm
        self.player1 = None
        self.player2 = None
        self.player3 = None 
        self.player4 = None
        

    # tạo số lượng đối tượng do người chơi chọn
    def install_player(self):
        self.clear_players(self.players_group)
        # print(self.number_player)
        if self.number_player_1 == True:  
            self.player1 = Player(1)
            self.players_group.add(self.player1)

        if self.number_player_2 == True:# or self.number_player == 3 or self.number_player == 4:
            self.player2 = Player(2)
            self.players_group.add(self.player2)

        if self.number_player_3 == True :#or self.number_player == 4:
            self.player3 = Player(3)
            self.players_group.add(self.player3)

        if self.number_player_4 == True:
            self.player4 = Player(4)
            self.players_group.add(self.player4)

    
    def draw_menu(self):
        # Vẽ nút và xử lý lựa chọn
        if self.p1p.draw(self.display_surface):
            # self.number_player_1 = True
            # self.p1p_selected = True#, self.p2p_selected, self.p3p_selected, self.p4p_selected = True, False, False, False
            self.number_player_1 = not self.number_player_1
            self.p1p_selected = self.number_player_1


        if self.p2p.draw(self.display_surface):
            self.number_player_2 = not self.number_player_2
            self.p2p_selected = self.number_player_2

        if self.p3p.draw(self.display_surface):
            self.number_player_3 = not self.number_player_3
            self.p3p_selected = self.number_player_3

        if self.p4p.draw(self.display_surface):
            self.number_player_4 = not self.number_player_4
            self.p4p_selected = self.number_player_4

        if self.back.draw(self.display_surface):
            return 'back'

        if self.next.draw(self.display_surface):
            return 'next'

        # Hiển thị lựa chọn số lượng người chơi
        if self.p1p_selected:
            self.display_surface.blit(self.chose_img, (355, 400))
        if self.p2p_selected:
            self.display_surface.blit(self.chose_img, (526.5, 400))
        if self.p3p_selected:
            self.display_surface.blit(self.chose_img, (697, 400))
        if self.p4p_selected:
            self.display_surface.blit(self.chose_img, (867, 400))
        
          # Không có hành động nào khác
    
    
