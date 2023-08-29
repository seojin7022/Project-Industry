import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, pos=(0, 0), surf=pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(groups)
        

        self.image = surf
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


        # Hello World!