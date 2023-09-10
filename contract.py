import pygame, os
from pygame._sdl2 import *
from settings import *
from gui import *


class Contract:
    def __init__(self, app) -> None:
        self.app = app
        
    def click(self, button):
        pass

    def run(self):
        pass

class ContractGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "contract_gui")
        self.frame_structure = {
            "UI_Contract": [{
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            }],

            "UI_QuestBox1": [{
                "position": (WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] / 2 + 150 * i - 150)
            } for i in range(3)],

            

        }

        self.button_structure = {
            "B_Accept": [{
                "position": (WINDOW_SIZE[0] / 2 + 210, WINDOW_SIZE[1] / 2 + 150 * i - 170)
            } for i in range(3)],

            "B_Cancel": [{
                "position": (WINDOW_SIZE[0] / 2 + 160, WINDOW_SIZE[1] / 2 + 150 * i - 170)
            } for i in range(3)],
        }

        self.load_guis()