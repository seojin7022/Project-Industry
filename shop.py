import pygame, os, json
from pygame._sdl2 import *
from settings import *
from gui import *

shop_items = {
    "Peel_Machine": 1000
}


class Shop:
    def __init__(self, app) -> None:
        self.app = app
        

    def run(self):
        pass

class ShopGUI(pygame.sprite.Group):
    def __init__(self, app) -> None:
        super().__init__()
        self.name = "shop_gui"
        self.frames = []
        self.buttons = []
        self.texts = []

        self.scroll = Scroll((1000, 650), direction="v")
        self.scroll.rect.center = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 100)

        self.app = app

        self.structure = {
            "UI_Shop.png": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            },

            "B_Cancel.png": {
                "position": (WINDOW_SIZE[0] / 2 + 350, WINDOW_SIZE[1] / 2 + 360)
            },

            "B_Purchase.png": {
                "position": (WINDOW_SIZE[0] / 2 + 590, WINDOW_SIZE[1] / 2 + 360)
            }

        }

        self.load_guis()

    def load_guis(self):
        for i in os.listdir(f"./gui/{self.name}"):
            if i == "button":
                for button in os.listdir(f"./gui/{self.name}/button"):
                    if button.endswith("_Hover.png"): continue
                    hover_img = None
                    
                    if os.path.exists(f"./gui/{self.name}/button/{button.split('.')[0] + '_Hover.png'}"):
                        
                        hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button.split('.')[0] + '_Hover.png'}")))
                        
                    newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}"))), hover_img)
                    newButton.name = button
                    newButton.rect.center = self.structure[button]["position"]
                    self.buttons.append(newButton)
            elif i == "frame":
                for frame in os.listdir(f"./gui/{self.name}/{i}"):
                    newFrame = Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/{i}/{frame}")))
                    newFrame.name = frame
                    newFrame.rect.center = self.structure[frame]["position"]
                    self.frames.append(newFrame)
        for button in os.listdir("./gui/edit_gui/button"):
            if "Machine" in button:
                newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/edit_gui/button/{button}"))), None)
                newButton.name = button.split(".")[0]
                self.scroll.add_children(newButton)
                self.buttons.append(newButton)
    def custom_draw(self):
        self.scroll.custom_draw()
        for frame in self.frames:
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)