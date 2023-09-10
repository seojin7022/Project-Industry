import pygame, os, json
from pygame._sdl2 import *
from settings import *
from objects import *
from gui import *

direction_list = {
    "R": "B",
    "B": "L",
    "L": "T",
    "T": "R",
    "RT": "BR",
    "BR": "LB",
    "LB": "TL",
    "TL": "RT",
    "RB": "BL",
    "BL": "LT",
    "LT": "TR",
    "TR": "RB"
    
}

def get_direction(dir, count):

    if dir == "RT" or dir == "RB" or dir == "R":
        return count
    else:
        key = ""
        for i in direction_list.keys():
            if direction_list[i] == dir:
                key = i
                break
        count = get_direction(key, count + 1)

    return count

class Edit:
    def __init__(self, conveyer: Conveyer, app) -> None:
        self.app = app
        self.conveyer = conveyer
        self.delete_mode = False
        self.delete_pos = (0, 0)
        self.r_pressed = False


    def click(self, button: Button):
        if button.name != "B_Delete":
            self.delete_mode = False

        if button.name == "UI_Edit_CVB_R":
            self.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction="R")
        elif button.name == "UI_Edit_CVB_RT":
            self.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-2.png"),self.app, direction="RT")
        elif button.name == "UI_Edit_CVB_RB":
            self.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-3.png"),self.app, direction="RB")
        elif "Machine" in button.name:
            self.conveyer = Machine(pygame.image.load(f"./img/Tiles/{button.name.replace('UI_Edit_', '')}.png"),self.app, name=button.name.replace('UI_Edit_', ''))
        elif button.name == "UI_Edit_Container":
            self.conveyer = SpecialPoint(pygame.image.load(f"./img/Tiles/Container.png"),self.app, "S")
        elif button.name == "UI_Edit_EndPoint":
            self.conveyer = SpecialPoint(pygame.image.load(f"./img/Tiles/T_Out.png"),self.app, "E")
                
        elif button.name == "B_Delete":
            if self.delete_mode:
                self.delete_mode = False
                self.conveyer = Conveyer(pygame.image.load("./img/Tiles/CVB-1.png"),self.app, direction="R")
            else:
                self.delete_mode = True
                self.conveyer = Conveyer(pygame.image.load("./img/Tiles/UI_Delete.png"),self.app, direction="R")
        else:
            self.delete_mode = False
        

    def run(self, floor_objects, offset):
        if self.conveyer != None:
            self.conveyer.image.alpha = 100
            self.conveyer.rect.topleft = offset
        for floor in floor_objects:
            if floor.real_rect.collidepoint(pygame.mouse.get_pos()):
                if self.conveyer != None:
                    self.conveyer.rect.topleft = floor.real_rect.topleft
                    self.conveyer.position = floor.position
                self.delete_pos = floor.position

        if type(self.conveyer) == Conveyer:
            keyboard = pygame.key.get_pressed()

            if keyboard[pygame.K_r] and not self.r_pressed:
                self.r_pressed = True
                self.conveyer.image.angle += 90
                self.conveyer.direction = direction_list[self.conveyer.direction]
            elif not keyboard[pygame.K_r]:
                self.r_pressed = False

        self.app[1].blit(self.conveyer.image, self.conveyer.rect)

class EditGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "edit_gui")
        

        BUTTON_SIZE = 97

        

        self.frame_structure = {
            "UI_Bottom": {
                "position": (WINDOW_SIZE[0] / 2, 950)
            },

        }

        self.button_structure = {
            "B_Close": {
                "position": (1765, 780)
            },
            "B_Delete": {
                "position": (1765 - BUTTON_SIZE, 780)
            },
        }

        self.text_structure = {
            "Rotate_text": {
                "font": "OTF_Bold.otf",
                "font-size": 25,
                "text": "회전: R",
                "position": (WINDOW_SIZE[0] / 2 + 600, 850),
                "color": (0, 0, 0)
            }
        }

        edit_scroll = Scroll((1700, 97))
        edit_scroll.rect.center = (WINDOW_SIZE[0] / 2, 920)

        self.scroll_structure = {
            "edit_scroll": edit_scroll
        }

        self.load_guis()

        
            