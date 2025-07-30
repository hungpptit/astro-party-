import math
from os.path import join
from os import walk
import pygame # type: ignore
import random
import math
import numpy as np
from os.path import join
pygame.font.init()
pygame.mixer.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 64
pygame.mixer.set_num_channels(10)  # Cho phép tối đa 10 kênh âm thanh





# Font chữ
font_path = join('..', 'AstroParty','lesson1', '04B_19.TTF')
font_start = pygame.font.Font(font_path,30)
font_titles = pygame.font.Font(font_path,70)