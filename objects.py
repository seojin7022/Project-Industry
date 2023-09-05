import pygame
from pygame._sdl2 import *
from settings import *



class Conveyer(pygame.sprite.Sprite):
    def __init__(self, surf,app, direction="R") -> None:
        super().__init__()
        
        
        self.direction = direction
        self.position = (0, 0)
        if type(surf) == Image:
            self.image = Image(surf.texture)
            self.image.angle = surf.angle
        else:
            self.image = Image(Texture.from_surface(app[1], surf))
        self.rect = self.image.get_rect()
        self.real_rect = self.rect.copy()

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, groups, name, app) -> None:
        super().__init__(groups)
        self.app = app
        self.name = name
        self.image = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./img/ingredients/{name}.png")))
        self.rect = self.image.get_rect()
        self.position = (1, 1)
        self.rect.topleft = (self.position[0] * TILE_SIZE / 4 + TILE_SIZE, self.position[1] * TILE_SIZE / 4 + TILE_SIZE)
        self.real_rect = self.rect.copy()