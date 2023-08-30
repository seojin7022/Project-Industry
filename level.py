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
        self.mouse_pos = pygame.mouse.get_pos()
        self.offset = (0, 0)

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
        
        
        

        if (mouse[0]):
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != self.mouse_pos:
                self.offset = (self.offset[0] + (current_mouse_pos[0] - self.prior_mouse_pos[0]) * 0.2,self.offset[1] + (current_mouse_pos[1] - self.prior_mouse_pos[1]) * 0.2)
            else:
                self.prior_mouse_pos = current_mouse_pos

        
        elif (mouse[0] == 0):
            self.prior_mouse_pos = pygame.mouse.get_pos()
            
        
        self.mouse_pos = pygame.mouse.get_pos()

    def run(self):
        self.drag()
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.offset)

class SortCamera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def custom_draw(self, offset):
        print(offset)
        for sprite in self.sprites():
            
            

            new_rect = sprite.rect.copy()
            new_rect.left += offset[0]
            new_rect.top += offset[1]
            self.display_surf.blit(sprite.image, new_rect)
            