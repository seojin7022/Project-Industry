import pygame, os, json, copy
from pygame._sdl2 import *
from settings import *
from tile import Tile
from pytmx.util_pygame_sdl2 import load_pygame_sdl2
from gui import Button, Frame, Text
from edit import *
from objects import Conveyer, Ingredient
from gamemath import *
from animation import *
from info import *



class Level:
    def __init__(self, app: [Window, Renderer, dict, bool]) -> None:
        self.app = app
        self.window = app[0]
        self.renderer = app[1]

        #Sprite Groups
        self.visible_sprites = SortCamera(app)
        self.floor_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.gui_sprites = MainGUI(app)
        self.edit_gui_sprites = EditGUI(app)
        self.ingredient_sprites = SortCamera(app)
        self.animation_sprites = AnimationController()
        self.info_gui_sprites = InfoGUI(app)

        #Mouse Control Values
        self.prior_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = pygame.mouse.get_pos()
        self.offset = (0, 0)
        self.mouse_pressed = False

        #Map
        self.map = [["0" for i in range(MAP_SIZE[0])] for j in range(MAP_SIZE[1])]
        self.map[0][0] = "S"
        self.map[5][5] = "E"
        self.startpoint = (0, 0)
        self.endpoint = (5, 5)

        #System
        self.info_system = Info(self.app)
        self.edit_system = Edit(Conveyer(pygame.image.load(f"./img/Tiles/CVB-1.png"), self.app), self.app)

        self.last_produce_time = pygame.time.get_ticks()

        self.mode = "None"

        self.modes = {
            "Edit": [self.edit_gui_sprites, self.edit_system],
            "Info": [self.info_gui_sprites, self.info_system]
        }

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
        self.isGuiCollide = False

        self.isGuiCollide = self.edit_gui_sprites.scroll.drag(mouse)
        
        if (mouse[2] and not self.isGuiCollide):
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != self.mouse_pos:
                self.offset = (self.offset[0] + int(clamp(50, (current_mouse_pos[0] - self.prior_mouse_pos[0]) * 0.1)),self.offset[1] + int(clamp(50, (current_mouse_pos[1] - self.prior_mouse_pos[1]) * 0.1)))
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
            for button in self.gui_sprites.buttons:
                button:Button
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.isGuiCollide = True
                    if button.name == "B_Edit.png" and self.mode != "Edit":
                        self.mode = "Edit"
                        self.edit_system.run(self.floor_sprites, self.offset)
                    elif button.name == "B_Info.png" and self.mode != "Info":
                        self.mode = "Info"
                        self.info_system.run()
            
            if self.mode == "Edit":
                for button in self.edit_gui_sprites.buttons:
                    button:Button
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.isGuiCollide = True
                        if button.name != "B_Delete.png":
                            self.edit_system.delete_mode = False

                        if button.name == "UI_Edit_CVB_R.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction="R")
                        elif button.name == "UI_Edit_CVB_RT.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-2.png"),self.app, direction="RT")
                        elif button.name == "UI_Edit_CVB_RB.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-3.png"),self.app, direction="RB")
                        elif button.name == "B_Delete.png":
                            if self.edit_system.delete_mode:
                                self.edit_system.delete_mode = False
                                self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction="R")
                            else:
                                self.edit_system.delete_mode = True
                                self.edit_system.conveyer = None
                        else:
                            self.mode = "None"
                            for button in self.edit_gui_sprites.buttons:
                                button.hover_out(self.app[1], self.animation_sprites)
                if not self.isGuiCollide: #컨베이어 벨트 설치
                    if self.edit_system.delete_mode:
                        
                        self.map[self.edit_system.delete_pos[0]][ self.edit_system.delete_pos[1]] = "0"
                        for sprite in self.visible_sprites.sprites():
                            if type(sprite) == Conveyer:
                                if sprite.position == self.edit_system.delete_pos:
                                    sprite.kill()
                        self.visible_sprites.remove()
                    else:
                        newConveyer = Conveyer(self.edit_system.conveyer.image,self.app,  direction=self.edit_system.conveyer.direction)
                        newConveyer.image.alpha = 255
                        newConveyer.position = self.edit_system.conveyer.position
                        self.map[newConveyer.position[0]][newConveyer.position[1]] = newConveyer.direction
                        newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                        self.visible_sprites.add(newConveyer)
                    
                    

        elif (mouse[0] == 0):
            self.mouse_pressed = False

    def hover(self):
        mouse = pygame.mouse.get_pos()

        for button in self.gui_sprites.buttons:
            button: Button
            if button.rect.collidepoint(mouse):
                button.hover(self.app[1], self.animation_sprites)
            else:
                button.hover_out(self.app[1], self.animation_sprites)

        if self.mode != "None":
            for button in self.modes[self.mode][0].buttons:
                
                button: Button
                if button.rect.collidepoint(mouse):
                    button.hover(self.app[1], self.animation_sprites)
                else:
                    button.hover_out(self.app[1], self.animation_sprites)

    def Edit(self):
        self.edit_system.run(self.floor_sprites, self.offset)

    def produce(self):
        if pygame.time.get_ticks() - self.last_produce_time > 1000:
            if self.startpoint[0] < MAP_SIZE[0] - 1:
                
                if not (self.map[self.startpoint[0] + 1][self.startpoint[1]] in ["0", "E"]):
                    Ingredient(self.ingredient_sprites, "Stone", self.app, position=(self.startpoint[0] + 1, self.startpoint[1]))
                    self.last_produce_time = pygame.time.get_ticks()

    def convey(self):
        for ingredient in self.ingredient_sprites.sprites():
            ingredient: Ingredient
            
            direction = self.map[ingredient.position[0]][ingredient.position[1]]
            if direction == "0":
                ingredient.kill()
                continue
            elif direction == "E":
                ingredient.kill()
                self.app[2]["Money"] += 100
                continue
            
            if len(direction) == 2:
                direction = direction[0]

                if direction == "R":
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
                if ingredient.rect.centerx >= (ingredient.position[0] + 1) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0] + 1][ingredient.position[1]][0]
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0] + 1, ingredient.position[1])
                    
            elif direction == "L": #왼쪽으로 갈때
                ingredient.rect.left -= 1
                if ingredient.rect.centerx <= (ingredient.position[0] + 1) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0] - 1][ingredient.position[1]][0]
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0] - 1, ingredient.position[1])
            elif direction == "T":
                ingredient.rect.top -= 1
                if ingredient.rect.centery <= (ingredient.position[1] + 1) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] - 1][0]
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] - 1)
            elif direction == "B":
                
                ingredient.rect.top += 1
                if ingredient.rect.centery >= (ingredient.position[1] + 1) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] + 1][0]
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] + 1)

            
                


    def run(self):
        self.isGuiCollide = False
        self.drag()
        self.click_button()
        self.animation_sprites.update()
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.offset)
        self.convey()
        self.produce()
        self.ingredient_sprites.custom_draw(self.offset)
        
        if self.mode == "Edit":
            self.Edit()
        elif self.mode == "Info":
            pass
        if self.mode != "None":
            self.modes[self.mode][0].custom_draw()
        self.gui_sprites.custom_draw()
        self.hover()

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

        BUTTON_SIZE = 97

        self.structure = {
            "B_Info.png": {
                "position": (10, BUTTON_SIZE * 2),
            },

            "B_Edit.png": {
                "position": (10, BUTTON_SIZE * 3),
            },

            "B_Bank.png": {
                "position": (10, BUTTON_SIZE * 4),
            },

            "B_Shop.png": {
                "position": (10, BUTTON_SIZE * 5),
            },

            "B_Menu.png": {
                "position": (1920 - BUTTON_SIZE, 7),
            },

            "B_Stock.png": {
                "position": (10, BUTTON_SIZE * 6)
            },

            

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/main_gui"):
            if i == "button":
                for button in os.listdir("./gui/main_gui/button"):
                    if button.endswith("_Hover.png"): continue
                    hover_img = None
                    
                    if os.path.exists(f"./gui/main_gui/button/{button.split('.')[0] + '_Hover.png'}"):
                        
                        hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/main_gui/button/{button.split('.')[0] + '_Hover.png'}")))
                        
                    newButton = Button(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/main_gui/button/{button}")), hover_img)
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
                        self.texts.append(Text(self.app, font, int(font_size), text, (int(position.split(",")[0]), int(position.split(",")[1]))))

    def custom_draw(self):
        for frame in self.frames:
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)

