import pygame, os, json
from settings import *
from tile import Tile
from pytmx.util_pygame import load_pygame
from gui import Button, Frame, Text

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()

        self.visible_sprites = SortCamera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.gui_sprites = MainGUI()

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
        self.gui_sprites.custom_draw()

class SortCamera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def custom_draw(self, offset):
        for sprite in self.sprites():
            
            

            new_rect = sprite.rect.copy()
            new_rect.left += offset[0]
            new_rect.top += offset[1]
            self.display_surf.blit(sprite.image, new_rect)


class MainGUI(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []
        self.buttons = []
        self.texts = []

        self.display_surf = pygame.display.get_surface()

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/main_gui"):
            if i == "button":
                for button in os.listdir("./gui/main_gui/button"):
                    print(os.path.exists(f"./gui/main_gui/button/{button}"))
                    self.buttons.append(Button(pygame.image.load(f"./gui/main_gui/button/{button}").convert_alpha()))
            elif i == "frame":
                for frame in os.listdir(f"./gui/main_gui/{i}"):
                    self.frames.append(Frame(pygame.image.load(f"./gui/main_gui/{i}/{frame}").convert_alpha()))
            elif i == "text":
                for text in os.listdir(f"./gui/main_gui/{i}"):
                    with open(f"./gui/main_gui/{i}/{text}", 'r') as text_data:
                        text_data = json.loads(text_data.read())
                        font = text_data["font"]
                        text = text_data["text"]
                        position = text_data["position"]
                        font_size = text_data["font-size"]
                        self.texts.append(Text(font, int(font_size), text, (int(position.split(",")[0]), int(position.split(",")[1]))))
                        print(map(int, position.split(",")))

    def custom_draw(self):
        for frame in self.frames:
            self.display_surf.blit(frame.image, (0, 0))

        for button in self.buttons:
            self.display_surf.blit(button.image, (0, 0))

        for text in self.texts:
            self.display_surf.blit(text.render(), text.position)