import pygame
from settings import *

class Conveyer(pygame.sprite.Sprite):
    def __init__(self, surf) -> None:
        super().__init__()
        self.direction = "R"
        self.position = (0, 0)

        self.image = surf
        self.rect = self.image.get_rect()
        self.real_rect = self.rect.copy()