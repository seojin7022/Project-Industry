import pygame
from settings import *



class Conveyer(pygame.sprite.Sprite):
    def __init__(self, surf, direction="R") -> None:
        super().__init__()
        self.direction = direction
        self.position = (0, 0)

        self.image = surf
        self.rect = self.image.get_rect()
        self.real_rect = self.rect.copy()

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, groups, name) -> None:
        super().__init__(groups)

        self.name = name
        self.image = pygame.image.load(f"./img/ingredients/{name}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.position = (1, 1)
        self.rect.topleft = (self.position[0] * TILE_SIZE / 4 + TILE_SIZE, self.position[1] * TILE_SIZE / 4 + TILE_SIZE)
        self.real_rect = self.rect.copy()