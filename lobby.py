import pygame, sys
from pygame._sdl2 import *
from settings import *
from gui import *
from animation import *


class Lobby:
    def __init__(self, app: [Window, Renderer]) -> None:
        self.app = app
        self.window = app[0]
        self.renderer = app[1]

        #Sprite Groups
        self.gui_sprites = MainGUI(app)
        self.gamerule_sprites = GameRuleGUI(app)
        self.animation_sprites = AnimationController()
        

        #Mouse Control Values
        self.prior_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = False

        self.gamerule_enabled = False

    def click_button(self):
        mouse = pygame.mouse.get_pressed()

        if (mouse[0] and not self.mouse_pressed):
            self.mouse_pressed = True
            if not self.gamerule_enabled:
                for button in self.gui_sprites.buttons:
                    button:Button
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.isGuiCollide = True
                        if button.name == "B_Start":
                            return True
                        elif button.name == "B_GameRule" and not self.gamerule_enabled:
                            self.gamerule_enabled = True

                        elif button.name == "B_Exit":
                            pygame.quit()
                            sys.exit()

            if self.gamerule_enabled:
                for button in self.gamerule_sprites.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button.name == "L_Arrow":
                            self.gamerule_sprites.mode -= 1
                            self.gamerule_sprites.mode = max(0, self.gamerule_sprites.mode)
                        elif button.name == "R_Arrow":
                            self.gamerule_sprites.mode += 1

                            if self.gamerule_sprites.mode == 4:
                                self.gamerule_enabled = False
                                self.gamerule_sprites.mode = 0
                        

        elif (mouse[0] == 0):
            self.mouse_pressed = False

    def hover(self):
        mouse = pygame.mouse.get_pos()
        
        if not self.gamerule_enabled:
            for button in self.gui_sprites.buttons:
                button: Button
                if button.rect.collidepoint(mouse):
                    button.hover(self.app[1], self.animation_sprites)
                else:
                    button.hover_out(self.app[1], self.animation_sprites)

    def run(self):
        self.isGuiCollide = False
        out = self.click_button()
        if out:
            return True
        self.animation_sprites.update()
        if not self.gamerule_enabled:
            self.gui_sprites.custom_draw()
        if self.gamerule_enabled:
            self.gamerule_sprites.custom_draw()
        self.hover()

class MainGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "lobby_gui")

        self.last_clock_time = pygame.time.get_ticks()

        self.frame_structure = {
            "Main": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            }
        }

        self.button_structure = {

            "B_Exit": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 350)
            },


            "B_GameRule": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 200)
            },

            "B_Start": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            },

        }

        self.load_guis()

class GameRuleGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "gamerule_gui")

        self.last_clock_time = pygame.time.get_ticks()

        self.modes = ["H_Main", "H_Shop", "H_Edit", "H_Con"]
        

        self.mode = 0

        self.frame_structure = {
            "H_Con": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            },

            "H_Edit": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            },

            "H_Main": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            },

            "H_Shop": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
            },
        }

        self.button_structure = {

            "L_Arrow": {
                "position": (WINDOW_SIZE[0] - 200, WINDOW_SIZE[1] - 100)
            },


            "R_Arrow": {
                "position": (WINDOW_SIZE[0] -100, WINDOW_SIZE[1] - 100)
            },

        }

        self.load_guis()

    def custom_draw(self):
        for frame in self.frames:
            if frame.name == self.modes[self.mode]:
                self.app[1].blit(frame.image, frame.rect)
        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)