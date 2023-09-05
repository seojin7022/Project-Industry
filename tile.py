import pygame
from pygame._sdl2 import *
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos=(0, 0),  position=(0, 0)) -> None:
        super().__init__(groups)
        
        
        self.image = Image(surf.texture)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.real_rect = self.rect.copy()
        self.position = position


        # Hello World!