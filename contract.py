import pygame, os
from pygame._sdl2 import *
from settings import *
from gui import *


class Contract:
    def __init__(self, app) -> None:
        self.app = app
        

    def run(self):
        pass

class ContractGUI(pygame.sprite.Group):
    def __init__(self, app) -> None:
        super().__init__()
        self.name = "contract_gui"
        self.frames = []
        self.buttons = []
        self.texts = []

        self.app = app

        self.frame_structure = {
            "UI_Contract.png": [{
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            }],

            "UI_QuestBox1.png": [{
                "position": (WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] / 2 + 150 * i - 150)
            } for i in range(3)],

            

        }

        self.button_structure = {
            "B_Accept.png": [{
                "position": (WINDOW_SIZE[0] / 2 + 210, WINDOW_SIZE[1] / 2 + 150 * i - 170)
            } for i in range(3)],

            "B_Cancel.png": [{
                "position": (WINDOW_SIZE[0] / 2 + 160, WINDOW_SIZE[1] / 2 + 150 * i - 170)
            } for i in range(3)],
        }

        self.load_guis()

    def load_guis(self):
        for button, v in self.button_structure.items():
            for pos in v:
                hover_img = None
                
                if os.path.exists(f"./gui/{self.name}/button/{button.split('.')[0] + '_Hover.png'}"):
                    
                    hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button.split('.')[0] + '_Hover.png'}")))
                    
                newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}"))), hover_img)
                newButton.name = button
                newButton.rect.center = pos["position"]
                self.buttons.append(newButton)

        for frame, v in self.frame_structure.items():
            for pos in v:
                newFrame = Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/frame/{frame}")))
                newFrame.name = frame
                newFrame.rect.center = pos["position"]
                self.frames.append(newFrame)

    def custom_draw(self):
        for frame in self.frames:
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)