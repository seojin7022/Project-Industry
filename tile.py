import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        