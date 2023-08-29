import pygame
from settings import *
from tile import Tile
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()

        self.visible_sprites = SortCamera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.prior_mouse_pos = pygame.mouse.get_pos()

        self.create_map()
    
    def create_map(self):
        tilemap = load_pygame("Tilemap/map.tmx")
        
        for layer in tilemap.layers:
            if hasattr(layer, 'data'):
                if layer.name == "Floor":
                    for x, y, surf in layer.tiles():
                        print((x * TILE_SIZE, y * TILE_SIZE))
                        Tile(self.visible_sprites, (x * TILE_SIZE, y * TILE_SIZE), surf)

    def drag(self):
        mouse = pygame.mouse.get_pressed()
        
        self.offset = (0, 0)
        self.prior_mouse_pos = pygame.mouse.get_pos()

        if (mouse[0]):
            current_mouse_pos = pygame.mouse.get_pos()
            self.offset = ((current_mouse_pos[0] - self.prior_mouse_pos[0]) * 0.2, (current_mouse_pos[1] - self.prior_mouse_pos[1]) * 0.2)

    def run(self):
        self.drag()
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.offset)

class SortCamera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def custom_draw(self, offset):
        for sprite in self.sprites():
            sprite.rect.left += offset[0]
            sprite.rect.top += offset[1]
            self.display_surf.blit(sprite.image, sprite.rect)