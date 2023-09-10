import pygame, os
from pygame._sdl2 import *
from settings import *
from animation import *

ingredient_money = {
    "Oak": [100, 200, 400, 1000]
}

ingredients = {
    "Oak": [pygame.image.load(f"./img/ingredients/Oak/{filename}") for filename in os.listdir("./img/ingredients/Oak")]
}

machine_count = {
    "Peel_Machine": 1,
}

class SpecialPoint(pygame.sprite.Sprite):
    def __init__(self, surf, app, name) -> None:
        super().__init__()
        self.position = (0, 0)
        self.name = name
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

class Machine(pygame.sprite.Sprite):
    def __init__(self, surf,app, name="Peel_Machine") -> None:
        super().__init__()
        
        self.name = name
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
        self.images = ingredients[name]
        self.count = 0
        self.money = ingredient_money[name][self.count]
        
        
        self.position = position

        self.image = Image(Texture.from_surface(app[1], self.images[self.count]))
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0] * TILE_SIZE + TILE_SIZE / 2, self.position[1] * TILE_SIZE + TILE_SIZE / 2)
        self.real_rect = self.rect.copy()

    def manufacture(self, count):
        if self.count + 1 == count:
            self.count += 1
            self.image = Image(Texture.from_surface(self.app[1], self.images[self.count]))
            self.money = ingredient_money[self.name][self.count]
