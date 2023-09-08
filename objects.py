import pygame
from pygame._sdl2 import *
from settings import *
from animation import *

class StartPoint(pygame.sprite.Sprite):
    def __init__(self, surf, app) -> None:
        super().__init__()
        self.position = (0, 0)

        if type(surf) == Image:
            self.image = Image(surf.texture)
            self.image.angle = surf.angle
        else:
            self.image = Image(Texture.from_surface(app[1], surf))
        self.rect = self.image.get_rect()
        self.real_rect = self.rect.copy()

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
    def __init__(self, groups, name, app, position=(1, 1)) -> None:
        super().__init__(groups)
        self.app = app
        self.name = name
        self.image = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./img/ingredients/{name}.png")))
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = (self.position[0] * TILE_SIZE + TILE_SIZE / 2, self.position[1] * TILE_SIZE + TILE_SIZE / 2)
        self.real_rect = self.rect.copy()