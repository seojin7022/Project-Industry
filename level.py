import pygame, threading, time
from pygame._sdl2 import *
from settings import *
from tile import Tile
from pytmx.util_pygame_sdl2 import load_pygame_sdl2
from gui import Button, Frame, Text
from edit import *
from objects import *
from gamemath import *
from animation import *
from info import *
from shop import *
from contract import *


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
        self.machine_sprites = SortCamera(app)
        self.shop_gui_sprites = ShopGUI(app)
        self.contract_gui_sprites = ContractGUI(app)
        

        #Mouse Control Values
        self.prior_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = pygame.mouse.get_pos()
        self.offset = (0, 0)
        self.mouse_pressed = False

        #Map
        self.map = self.app[2]["Map"]
        self.machine_map = self.app[2]["MachineMap"]
        self.map[0][0] = "S"
        self.map[5][5] = "E"
        self.startpoint = (0, 0)
        self.endpoint = (5, 5)

        #System
        self.info_system = Info(self.app)
        self.edit_system = Edit(Conveyer(pygame.image.load(f"./img/Tiles/CVB-1.png"), self.app), self.app)
        self.shop_system = Shop(app)
        self.contract_system = Contract(app)

        self.last_produce_time = pygame.time.get_ticks()

        self.mode = "None"

        self.modes = {
            "Edit": [self.edit_gui_sprites, self.edit_system],
            "Info": [self.info_gui_sprites, self.info_system],
            "Shop": [self.shop_gui_sprites, self.shop_system],
            "Contract": [self.contract_gui_sprites, self.contract_system],
        }

        self.ui_no_machine = pygame.image.load("./gui/UI_No_Machine.png")

        self.create_map()
        
    
    def create_map(self):
        tilemap = load_pygame_sdl2(self.app[1], "Tilemap/map.tmx")
        
        for layer in tilemap.layers:
            if hasattr(layer, 'data'):
                if layer.name == "Floor":
                    for x, y, surf in layer.tiles():
                        Tile([self.visible_sprites, self.floor_sprites], surf, (x * TILE_SIZE, y * TILE_SIZE), (x, y))

        for i in range(MAP_SIZE[1]):
            for j in range(MAP_SIZE[0]):
                if self.map[i][j] == "S":
                    newConveyer = Conveyer(pygame.image.load("./img/Tiles/Container.png"),self.app)
                    newConveyer.position = (i, j)
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                elif self.map[i][j] == "E":
                    newConveyer = Conveyer(pygame.image.load("./img/Tiles/T_Out.png"),self.app)
                    newConveyer.position = (i, j)
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                elif self.map[i][j] != "0" and len(self.map[i][j]) == 1:
                    newConveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction=self.map[i][j])
                    newConveyer.image.angle = 90 * get_direction(self.map[i][j], 0)
                    newConveyer.position = (i, j)
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                elif self.map[i][j] in ["RT", "BR", "LB", "TL"]:
                    newConveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-2.png"),self.app, direction=self.map[i][j])
                    newConveyer.image.angle = 90 * get_direction(self.map[i][j], 0)
                    newConveyer.position = (i, j)
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
                elif self.map[i][j] in ["RB", "BL", "LT", "TR"]:
                    newConveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-3.png"),self.app, direction=self.map[i][j])
                    newConveyer.image.angle = 90 * get_direction(self.map[i][j], 0)
                    newConveyer.position = (i, j)
                    newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                    self.visible_sprites.add(newConveyer)
        for i in range(MAP_SIZE[1]):
            for j in range(MAP_SIZE[0]):
                if self.machine_map[i][j] != "0":
                    newMachine = Machine(pygame.image.load(f"./img/Tiles/{self.machine_map[i][j]}.png"), self.app, name=self.machine_map[i][j])
                    newMachine.position = (i, j)
                    newMachine.rect.topleft = (newMachine.position[0] * TILE_SIZE, newMachine.position[1] * TILE_SIZE)
                    self.machine_sprites.add(newMachine)

    def drag(self):
        mouse = pygame.mouse.get_pressed()
        self.isGuiCollide = False

        if self.mode != "None":
            for scroll in self.modes[self.mode][0].scrolls:
                self.isGuiCollide = scroll.drag(mouse)
                
        
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
                    if button.name == "B_Edit" and self.mode != "Edit":
                        self.mode = "Edit"
                        self.edit_system.run(self.floor_sprites, self.offset)
                    elif button.name == "B_Info" and self.mode != "Info":
                        self.mode = "Info"
                        self.info_system.run()
                    elif button.name == "B_Shop" and self.mode != "Shop":
                        self.mode = "Shop"
                        self.shop_system.run()
                    elif button.name == "B_Contract" and self.mode != "Contract":
                        self.mode = "Contract"
                        self.contract_system.run()

            if self.mode != "None":
                for button in self.modes[self.mode][0].buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.isGuiCollide = True
                        self.modes[self.mode][1].click(button)
                        if button.name == "B_Close":
                            self.mode = "None"
                            button.hover_out(self.renderer, self.animation_sprites)
            
            
                
            if not self.isGuiCollide and self.mode == "Edit": #컨베이어 벨트 설치
                if self.edit_system.delete_mode:

                    if self.machine_map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]] != "0":

                        for sprite in self.machine_sprites.sprites():
                            if type(sprite) == Machine:
                                if sprite.position == self.edit_system.delete_pos:
                                    sprite.kill()
                                    self.app[2]["Machines"][self.machine_map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]]] += 1
                        self.machine_map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]] = "0"
                    else:
                    
                        self.map[self.edit_system.delete_pos[0]][ self.edit_system.delete_pos[1]] = "0"
                        for sprite in self.visible_sprites.sprites():
                            if type(sprite) == Conveyer:
                                if sprite.position == self.edit_system.delete_pos:
                                    sprite.kill()
                else:
                    if type(self.edit_system.conveyer) == Machine:
                        if not self.map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]] in ["0","E", "S"] and self.machine_map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]] == "0":
                            if self.app[2]["Machines"][self.edit_system.conveyer.name.replace("UI_Edit_", "")] > 0:
                                newMachine = Machine(self.edit_system.conveyer.image, self.app, name=self.edit_system.conveyer.name)
                                newMachine.image.alpha = 255
                                newMachine.position = self.edit_system.conveyer.position
                                self.machine_map[newMachine.position[0]][newMachine.position[1]] = newMachine.name
                                newMachine.rect.topleft = (newMachine.position[0] * TILE_SIZE, newMachine.position[1] * TILE_SIZE)
                                self.machine_sprites.add(newMachine)
                                self.app[2]["Machines"][self.edit_system.conveyer.name.replace("UI_Edit_", "")] -= 1
                            else:
                                
                                def a(obj):
                                    time.sleep(1)
                                    self.edit_gui_sprites.frames.remove(obj)
                                    del obj
                                    

                                UI_No_Machine = Frame(Image(Texture.from_surface(self.renderer, self.ui_no_machine)))
                                UI_No_Machine.rect
                                UI_No_Machine.rect.bottomleft = pygame.mouse.get_pos()
                                UI_No_Machine.animation = Animation(UI_No_Machine.image)
                                UI_No_Machine.image.alpha = 0
                                UI_No_Machine.animation.add_property("Alpha", 255, 300, 0)
                                self.edit_gui_sprites.frames.append(UI_No_Machine)
                                self.animation_sprites.add(UI_No_Machine)
                                threading.Thread(target=a, kwargs={"obj": UI_No_Machine}).start()
                                
                    else:
                        if self.map[self.edit_system.delete_pos[0]][self.edit_system.delete_pos[1]] == "0":
                            newConveyer = Conveyer(self.edit_system.conveyer.image,self.app,  direction=self.edit_system.conveyer.direction)
                            newConveyer.image.alpha = 255
                            newConveyer.position = self.edit_system.conveyer.position
                            self.map[newConveyer.position[0]][newConveyer.position[1]] = newConveyer.direction
                            newConveyer.rect.topleft = (newConveyer.position[0] * TILE_SIZE, newConveyer.position[1] * TILE_SIZE)
                            self.visible_sprites.add(newConveyer)

            if self.mode == "Shop":
                self.shop_gui_sprites.update_select(self.shop_system.selected_machine, self.shop_system.select_count)
            
            elif self.mode == "Contract":
                self.contract_gui_sprites.update_contract(self.contract_system.easy_contract, self.contract_system.normal_contract, self.contract_system.hard_contract)
            
            

                        

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
                    Ingredient(self.ingredient_sprites, "Oak", self.app, position=(self.startpoint[0] + 1, self.startpoint[1]))
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
                self.app[2]["Inventory"][ingredient.name + str(ingredient.count)] += 1
                continue
            
            if len(direction) == 2:
                direction = direction[0]

                if direction == "R":
                    if ingredient.rect.centerx + 1 >= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 2):
                        
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "L":
                    if ingredient.rect.centerx - 1 <= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 2):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "T":
                    if ingredient.rect.centery - 1 <= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 2):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
                elif direction == "B":
                    if ingredient.rect.centery + 1 >= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 2):
                        direction = self.map[ingredient.position[0]][ingredient.position[1]][1]
            
            

            if direction == "R": #오른쪽으로 갈때
                ingredient.rect.left += 1
                if ingredient.rect.centerx >= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0] + 1][ingredient.position[1]][0]
                    if self.machine_map[ingredient.position[0]][ingredient.position[1]] != "0":
                        ingredient.manufacture(machine_count[self.machine_map[ingredient.position[0]][ingredient.position[1]]])
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0] + 1, ingredient.position[1])
                    else:
                        ingredient.kill()

                    
                    
            elif direction == "L": #왼쪽으로 갈때
                ingredient.rect.left -= 1
                if ingredient.rect.centerx <= (ingredient.position[0]) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0] - 1][ingredient.position[1]][0]
                    if self.machine_map[ingredient.position[0]][ingredient.position[1]] != "0":
                        ingredient.manufacture(machine_count[self.machine_map[ingredient.position[0]][ingredient.position[1]]])
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0] - 1, ingredient.position[1])
                    else:
                        ingredient.kill()
            elif direction == "T":
                ingredient.rect.top -= 1
                if ingredient.rect.centery <= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] - 1][0]
                    if self.machine_map[ingredient.position[0]][ingredient.position[1]] != "0":
                        ingredient.manufacture(machine_count[self.machine_map[ingredient.position[0]][ingredient.position[1]]])
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] - 1)
                    else:
                        ingredient.kill()
            elif direction == "B":
                
                ingredient.rect.top += 1
                if ingredient.rect.centery >= (ingredient.position[1]) *TILE_SIZE + (TILE_SIZE / 2):
                    newDirection = self.map[ingredient.position[0]][ingredient.position[1] + 1][0]
                    if self.machine_map[ingredient.position[0]][ingredient.position[1]] != "0":
                        ingredient.manufacture(machine_count[self.machine_map[ingredient.position[0]][ingredient.position[1]]])
                    if newDirection == direction or newDirection == "0" or newDirection == "E":
                        ingredient.position = (ingredient.position[0], ingredient.position[1] + 1)
                    else:
                        ingredient.kill()
                


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
        self.machine_sprites.custom_draw(self.offset)
        if self.mode == "Edit":
            self.Edit()
        elif self.mode == "Info":
            pass
        if self.mode != "None":
            self.modes[self.mode][0].custom_draw()
        self.gui_sprites.update_money()
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


class MainGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "main_gui")
        BUTTON_SIZE = 97

        self.text_structure = {
            "Clock": {
                "font": "OTF_Bold.otf",
                "font-size": 32,
                "position": (30, 30),
                "color": (0, 0, 0),
                "text": "01월 01일 11:30"
            },

            "Money": {
                "font": "OTF_Bold.otf",
                "font-size": 32,
                "position": (800, 30),
                "color": (200, 200, 0),
                "text": "0"
            }
        }

        self.frame_structure = {
            "UI_Topbar": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            }
        }

        self.button_structure = {
            "B_Info": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 2),
            },

            "B_Bank": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 3),
            },

            "B_Shop": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 4),
            },

            "B_Stock": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 5),
            },

            "B_Menu": {
                "position": (1915 -  BUTTON_SIZE / 2, BUTTON_SIZE / 2 + 5),
            },

            "B_Edit": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 6)
            },

            "B_Contract": {
                "position": (BUTTON_SIZE / 2, BUTTON_SIZE * 7)
            }
        }

        self.load_guis()

    
    def update_money(self):
        for text in self.texts:
            if text.name == "Money":
                text.text = str(self.app[2]["Money"])