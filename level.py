import pygame, os, json
from pygame._sdl2 import *
from settings import *
from tile import Tile
from pytmx.util_pygame_sdl2 import load_pygame_sdl2
from gui import Button, Frame, Text
from edit import Edit, EditGUI
from objects import Conveyer, Ingredient
from gamemath import *

class Level:
    def __init__(self, app) -> None:
        self.app = app
        self.window = app[0]
        self.renderer = app[1]

        self.visible_sprites = SortCamera(app)
        self.floor_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.gui_sprites = MainGUI(app)
        self.edit_gui_sprites = EditGUI(app)
        self.ingredient_sprites = SortCamera(app)



        self.prior_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = pygame.mouse.get_pos()
        self.offset = (0, 0)

        self.map = [["0" for i in range(MAP_SIZE[0])] for j in range(MAP_SIZE[1])]

        self.mouse_pressed = False

        self.edit_system = Edit(Conveyer(pygame.image.load(f"./img/Tiles/CVB-1.png"), self.app), self.app)
    
        
        Ingredient([self.visible_sprites, self.ingredient_sprites], "Stone", self.app)

        self.create_map()
        
    
    def create_map(self):
        tilemap = load_pygame_sdl2(self.app[1], "Tilemap/map.tmx")
        
        for layer in tilemap.layers:
            if hasattr(layer, 'data'):
                if layer.name == "Floor":
                    for x, y, surf in layer.tiles():
                        Tile([self.visible_sprites, self.floor_sprites], surf, (x * TILE_SIZE, y * TILE_SIZE), (x, y))

    def drag(self):
        mouse = pygame.mouse.get_pressed()
        
        
        
        
        isGuiCollide = False

        isGuiCollide = self.edit_gui_sprites.scroll.drag(mouse)
        
        if (mouse[2] and not isGuiCollide):
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != self.mouse_pos:
                self.offset = (self.offset[0] + clamp(50, (current_mouse_pos[0] - self.prior_mouse_pos[0]) * 0.1),self.offset[1] + clamp(50, (current_mouse_pos[1] - self.prior_mouse_pos[1]) * 0.1))
                self.offset = (max(min(TILE_SIZE * 3, self.offset[0]), TILE_SIZE * -18), max(min(TILE_SIZE * 3, self.offset[1]), TILE_SIZE * -24))
            else:
                self.prior_mouse_pos = current_mouse_pos

        
        elif (mouse[2] == 0):
            self.prior_mouse_pos = pygame.mouse.get_pos()
            
        
        self.mouse_pos = pygame.mouse.get_pos()

    def click_button(self):
        mouse = pygame.mouse.get_pressed()

        if (mouse[0] and not self.mouse_pressed):
            self.mouse_pressed = True
            isGuiCollide = False
            for button in self.gui_sprites.buttons:
                button:Button
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    isGuiCollide = True
                    if button.name == "UI_E.png" and not self.gui_sprites.isEdit:
                        self.gui_sprites.isEdit = True
                        self.edit_system.run(self.floor_sprites, self.offset)
                    elif button.name == "UI_E.png" and self.gui_sprites.isEdit:
                        self.gui_sprites.isEdit = False
            
            if self.gui_sprites.isEdit:
                for button in self.edit_gui_sprites.buttons:
                    button:Button
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        isGuiCollide = True
                        if button.name == "UI_Conveyer_R.png":
                            
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction="R")
                        elif button.name == "UI_Conveyer_RT.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-2.png"),self.app, direction="RT")
                        elif button.name == "UI_Conveyer_RB.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-3.png"),self.app, direction="RB")
                        else:
                            self.gui_sprites.isEdit = False
                if not isGuiCollide: #컨베이어 벨트 설치
                    newConveyer = Conveyer(self.edit_system.conveyer.image,self.app,  direction=self.edit_system.conveyer.direction)
                    newConveyer.image.alpha = 255
                    newConveyer.position = self.edit_system.conveyer.position
                    self.map[newConveyer.position[0]][newConveyer.position[1]] = newConveyer.direction
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                    Ingredient([self.visible_sprites, self.ingredient_sprites], "Stone", self.app)
                    
                    

        elif (mouse[0] == 0):
            self.mouse_pressed = False

    def Edit(self):
        self.edit_system.run(self.floor_sprites, self.offset)

    def convey(self):
        for ingredient in self.ingredient_sprites.sprites():
            ingredient: Ingredient
            direction = self.map[ingredient.position[0]][ingredient.position[1]]

            
            if len(direction) == 2:
                direction = direction[0]

                if direction == "R":
                    print(ingredient.rect.left, (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 4))
                    if ingredient.rect.left + 1 >= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 4):
                        
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "L":
                    if ingredient.rect.left - 1 <= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 4):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "T":
                    if ingredient.rect.top - 1 <= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 4):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "B":
                    if ingredient.rect.top + 1 >= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 4):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
            

            if direction == "R": #오른쪽으로 갈때
                ingredient.rect.left += 1
                if ingredient.rect.left >= ingredient.position[0] *TILE_SIZE + (TILE_SIZE / 4):
                    newDirection = self.map[ingredient.position[0] + 1][ingredient.position[1]][0]
                    if newDirection == direction or newDirection == "0":
                        ingredient.position = (ingredient.position[0] + 1, ingredient.position[1])
                    
            elif direction == "L": #왼쪽으로 갈때
                ingredient.rect.left -= 1
                if ingredient.rect.left <= ingredient.position[0] * TILE_SIZE + (TILE_SIZE / 4):
                    newDirection = self.map[ingredient.position[0] - 1][ingredient.position[1]][0]
                    if newDirection == direction or newDirection == "0":
                        ingredient.position = (ingredient.position[0] - 1, ingredient.position[1])
            elif direction == "T":
                ingredient.rect.top -= 1
                if ingredient.rect.top <= ingredient.position[1] * TILE_SIZE + (TILE_SIZE / 4):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] - 1][0]
                    if newDirection == direction or newDirection == "0":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] - 1)
            elif direction == "B":
                
                ingredient.rect.top += 1
                if ingredient.rect.top >= ingredient.position[1] * TILE_SIZE + (TILE_SIZE / 4):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] + 1][0]
                    if newDirection == direction or newDirection == "0":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] + 1)

            
                


    def run(self):
        self.drag()
        self.click_button()
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.offset)
        self.convey()
        self.ingredient_sprites.custom_draw(self.offset)
        if self.gui_sprites.isEdit:
            self.Edit()
            self.edit_gui_sprites.custom_draw()
        self.gui_sprites.custom_draw()

class SortCamera(pygame.sprite.Group):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def custom_draw(self, offset):
        for sprite in self.sprites():
            newRect = sprite.rect.copy()
            newRect.topleft = (sprite.rect.left + offset[0], sprite.rect.top + offset[1])
            self.app[1].blit(sprite.image, newRect)
            sprite.real_rect.topleft = (sprite.rect.left + offset[0], sprite.rect.top + offset[1])


class MainGUI(pygame.sprite.Group):
    def __init__(self, app) -> None:
        super().__init__()
        self.frames = []
        self.buttons = []
        self.texts = []

        self.app = app

        self.isEdit = False

        BUTTON_SIZE = 97

        self.structure = {
            "UI_Bank.png": {
                "position": (10, BUTTON_SIZE * 2),
            },

            "UI_E.png": {
                "position": (10, BUTTON_SIZE * 3),
            },

            "UI_Finance.png": {
                "position": (10, BUTTON_SIZE * 4),
            },

            "UI_Info.png": {
                "position": (10, BUTTON_SIZE * 5),
            },

            "UI_Menu.png": {
                "position": (1920 - BUTTON_SIZE, 7),
            },

            "UI_Store.png": {
                "position": (10, BUTTON_SIZE * 6)
            },

            

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/main_gui"):
            if i == "button":
                for button in os.listdir("./gui/main_gui/button"):
                    newButton = Button(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/main_gui/button/{button}")))
                    newButton.name = button
                    newButton.rect.topleft = self.structure[button]["position"]
                    self.buttons.append(newButton)
            elif i == "frame":
                for frame in os.listdir(f"./gui/main_gui/{i}"):
                    self.frames.append(Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/main_gui/{i}/{frame}"))))
            elif i == "text":
                for text in os.listdir(f"./gui/main_gui/{i}"):
                    with open(f"./gui/main_gui/{i}/{text}", 'r') as text_data:
                        text_data = json.loads(text_data.read())
                        font = text_data["font"]
                        text = text_data["text"]
                        position = text_data["position"]
                        font_size = text_data["font-size"]
                        self.texts.append(Text(font, int(font_size), text, (int(position.split(",")[0]), int(position.split(",")[1]))))

    def custom_draw(self):
        for frame in self.frames:
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)

