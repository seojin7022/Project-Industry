import pygame, os, json, math
from settings import *
from tile import Tile
from pytmx.util_pygame import load_pygame
from gui import Button, Frame, Text
from edit import Edit
from objects import Conveyer, Ingredient

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()

        self.visible_sprites = SortCamera()
        self.floor_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.gui_sprites = MainGUI()
        self.edit_gui_sprites = EditGUI()
        self.ingredient_sprites = SortCamera()

        self.prior_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = pygame.mouse.get_pos()
        self.offset = (0, 0)

        self.map = [["0" for i in range(MAP_SIZE[0])] for j in range(MAP_SIZE[1])]

        self.mouse_pressed = False

        self.edit_system = Edit(Conveyer(pygame.image.load(f"./img/Tiles/CVB-1.png").convert()))

        Ingredient([self.visible_sprites, self.ingredient_sprites], "Stone")

        self.create_map()
        
    
    def create_map(self):
        tilemap = load_pygame("Tilemap/map.tmx")
        
        for layer in tilemap.layers:
            if hasattr(layer, 'data'):
                if layer.name == "Floor":
                    for x, y, surf in layer.tiles():
                        Tile([self.visible_sprites, self.floor_sprites], (x * TILE_SIZE, y * TILE_SIZE), surf, (x, y))

    def drag(self):
        mouse = pygame.mouse.get_pressed()
        
        
        def clamp(x, y):
            return max(min(x, y), -x)
        
        if (mouse[2]):
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
                            
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png").convert(), direction="R")
                        elif button.name == "UI_Conveyer_RT.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-2.png").convert(), direction="RT")
                        elif button.name == "UI_Conveyer_RB.png":
                            self.edit_system.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-3.png").convert(), direction="RB")
                        else:
                            self.gui_sprites.isEdit = False
                if not isGuiCollide: #컨베이어 벨트 설치
                    newConveyer = Conveyer(pygame.Surface.copy(self.edit_system.conveyer.image), direction=self.edit_system.conveyer.direction)
                    newConveyer.image.set_alpha(255)
                    newConveyer.position = self.edit_system.conveyer.position
                    self.map[newConveyer.position[0]][newConveyer.position[1]] = newConveyer.direction
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                    
                    

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
    def __init__(self) -> None:
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def custom_draw(self, offset):
        for sprite in self.sprites():
            self.display_surf.blit(sprite.image, (sprite.rect.left + offset[0], sprite.rect.top + offset[1]))
            sprite.real_rect.topleft = (sprite.rect.left + offset[0], sprite.rect.top + offset[1])


class MainGUI(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []
        self.buttons = []
        self.texts = []

        self.display_surf = pygame.display.get_surface()

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
            }

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/main_gui"):
            if i == "button":
                for button in os.listdir("./gui/main_gui/button"):
                    newButton = Button(pygame.image.load(f"./gui/main_gui/button/{button}").convert_alpha())
                    newButton.name = button
                    newButton.rect.topleft = self.structure[button]["position"]
                    self.buttons.append(newButton)
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

    def custom_draw(self):
        for frame in self.frames:
            self.display_surf.blit(frame.image, frame.rect)

        for button in self.buttons:
            self.display_surf.blit(button.image, button.rect)

        for text in self.texts:
            self.display_surf.blit(text.render(), text.position)

class EditGUI(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []
        self.buttons = []
        self.texts = []

        self.display_surf = pygame.display.get_surface()

        BUTTON_SIZE = 97

        self.structure = {
            "UI_Conveyer_R.png": {
                "position": (200, 890)
            },

            "UI_Conveyer_RT.png": {
                "position": (400, 890)
            },
            "UI_Conveyer_RB.png": {
                "position": (600, 890)
            },
            "UI_Close.png": {
                "position": (1765, 780)
            },

            "UI_Bottom.png": {
                "position": (50, 865)
            },

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/edit_gui"):
            if i == "button":
                for button in os.listdir("./gui/edit_gui/button"):
                    newButton = Button(pygame.image.load(f"./gui/edit_gui/button/{button}").convert_alpha())
                    newButton.name = button
                    newButton.rect.topleft = self.structure[button]["position"]
                    self.buttons.append(newButton)
            elif i == "frame":
                for frame in os.listdir(f"./gui/edit_gui/{i}"):
                    newFrame = Frame(pygame.image.load(f"./gui/edit_gui/{i}/{frame}").convert_alpha())
                    newFrame.name = frame
                    newFrame.rect.topleft = self.structure[frame]["position"]
                    self.frames.append(newFrame)
            elif i == "text":
                for text in os.listdir(f"./gui/edit_gui/{i}"):
                    with open(f"./gui/edit_gui/{i}/{text}", 'r') as text_data:
                        text_data = json.loads(text_data.read())
                        font = text_data["font"]
                        text = text_data["text"]
                        position = text_data["position"]
                        font_size = text_data["font-size"]
                        self.texts.append(Text(font, int(font_size), text, (int(position.split(",")[0]), int(position.split(",")[1]))))

    def custom_draw(self):
        for frame in self.frames:
            self.display_surf.blit(frame.image, frame.rect)

        for button in self.buttons:
            self.display_surf.blit(button.image, button.rect)

        for text in self.texts:
            self.display_surf.blit(text.render(), text.position)