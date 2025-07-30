import pygame
from os.path import join

click_mouse = pygame.mixer.Sound(join('..', 'AstroParty','lesson1','sound', 'menu-click1.mp3'))

click_mouse.set_volume(1)  # Đặt âm lượng (0.0 đến 1.0), max là 1 nếu đặt lớn hơn thì pygame tự set về 1

class Button():
    def __init__(self, x, y, image): # lấy x,y là tạo độ của nút
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # để kiểm tra nhấn nút 1 lần thôi
    def draw(self, surface):
        action = False # chức năng liên quan đến phân biệt 2 nút, đây không phải là 1 biến thực thể nên ko cần self chấm self.
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
                self.clicked = True
                action = True
                click_mouse.play()
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False   # để có thể tái kích hoạt nút
        # vẽ nút trên màn hình
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
