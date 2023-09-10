import pygame, os, json
from pygame._sdl2 import *
from settings import *
from objects import Conveyer
from gui import *


class Info:
    def __init__(self, app) -> None:
        self.app = app

    def click(self, button):
        pass
        

    def run(self):
        pass

class InfoGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "info_gui")


        self.frame_structure = {
            "UI_Info": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            },
        }

        self.button_structure = {
            "B_Close": {
                "position": (WINDOW_SIZE[0] / 2 + 390, WINDOW_SIZE[1] / 2 - 150)
            }
        }

        self.load_guis()