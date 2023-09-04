import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, pos=(0, 0), surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), position=(0, 0)) -> None:
        super().__init__(groups)
        
        
        self.image = surf
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.real_rect = self.rect.copy()
        self.position = position


        # Hello World!