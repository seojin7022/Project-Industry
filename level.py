import pygame
from settings import *

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    
    def create_map(self):
        pass

    def run(self):
        pass