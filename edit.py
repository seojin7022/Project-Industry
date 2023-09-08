import pygame, os, json
from pygame._sdl2 import *
from settings import *
from objects import Conveyer
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

class Edit:
    def __init__(self, conveyer: Conveyer, app) -> None:
        self.app = app
        self.conveyer = conveyer
        self.delete_mode = False
        self.delete_pos = (0, 0)
        self.r_pressed = False
        

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

        if self.conveyer != None:
            keyboard = pygame.key.get_pressed()

            if keyboard[pygame.K_r] and not self.r_pressed:
                self.r_pressed = True
                self.conveyer.image.angle += 90
                self.conveyer.direction = direction_list[self.conveyer.direction]
            elif not keyboard[pygame.K_r]:
                self.r_pressed = False

            self.app[1].blit(self.conveyer.image, self.conveyer.rect)

class EditGUI(pygame.sprite.Group):
    def __init__(self, app) -> None:
        super().__init__()
        self.frames = []
        self.buttons = []
        self.texts = []
        self.scroll = Scroll((1800, 97))
        self.scroll.rect.topleft = (50, 900)

        self.app = app

        BUTTON_SIZE = 97

        

        self.structure = {
            "UI_Conveyer_R.png": {
                "position": (200, 890),
            },

            "UI_Conveyer_RT.png": {
                "position": (400, 890)
            },
            "UI_Conveyer_RB.png": {
                "position": (600, 890)
            },
            "B_Close.png": {
                "position": (1765, 780)
            },
            "B_Delete.png": {
                "position": (1765 - BUTTON_SIZE, 780)
            },
            "UI_Bottom.png": {
                "position": (50, 840)
            },

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir("./gui/edit_gui"):
            if i == "button":
                for button in os.listdir("./gui/edit_gui/button"):
                    if button.endswith("_Hover.png"): continue
                    hover_img = None
                    
                    if os.path.exists(f"./gui/edit_gui/button/{button.split('.')[0] + '_Hover.png'}"):
                        
                        hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/edit_gui/button/{button.split('.')[0] + '_Hover.png'}")))
                        
                    newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/edit_gui/button/{button}"))), hover_img)
                    newButton.name = button
                    if button[0] == "B":
                        newButton.rect.topleft = self.structure[button]["position"]
                        self.buttons.append(newButton)
                    else:
                        self.scroll.add_children(newButton)
                        self.buttons.append(newButton)
            elif i == "frame":
                for frame in os.listdir(f"./gui/edit_gui/{i}"):
                    newFrame = Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/edit_gui/{i}/{frame}")))
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
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)

        self.scroll.custom_draw()

        for child in self.scroll.children:
            self.app[1].blit(child.image, child.rect)