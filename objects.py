import pygame
from settings import *

class Conveyer(pygame.sprite.Sprite):
    def __init__(self, surf) -> None:
        self.direction = "R"
        self.position = (0, 0)

        self.image = surf
        self.rect = self.image.get_rect()