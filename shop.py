import pygame
from pygame._sdl2 import *
from settings import *
from gui import *


shop_select_images = {}

for machine in shop_items.keys():
    shop_select_images.update({f"{machine}": pygame.image.load(f"./gui/shop_gui/frame/{machine}_Select.png")})


class Shop:
    def __init__(self, app) -> None:
        self.app = app
        self.selected_machine = None
        self.select_count = 1

    def click(self, button):
        if "Machine" in button.name:
            self.selected_machine = button.name

        if button.name == "B_Close":
            self.selected_machine = None
            self.select_count = 1
        elif button.name == "B_NumDown":
            self.select_count = max(1, self.select_count - 1)
        elif button.name == "B_NumUp":
            self.select_count = min(99, self.select_count + 1)
        elif button.name == "B_Purchase":
            if self.app[2]["Money"] >= shop_items[self.selected_machine] * self.select_count:
                if self.app[2]["Machines"].get(self.selected_machine):
                    self.app[2]["Machines"][self.selected_machine] += self.select_count
                else:
                    self.app[2]["Machines"].update({f"{self.selected_machine}": self.select_count})
                self.app[2]["Money"] -= shop_items[self.selected_machine] * self.select_count
                self.select_count = 1
            

    def run(self):
        pass

class ShopGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "shop_gui")
        self.name = "shop_gui"

        self.selected_machine = None
        self.selected_machine_position = (WINDOW_SIZE[0] / 2 + 600, WINDOW_SIZE[1] / 2 - 200)

        self.select_count = 1

        

        self.frame_structure = {
            "UI_Shop": {
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            },

            "UI_Num": {
                "position": (WINDOW_SIZE[0] / 2 + 650, WINDOW_SIZE[1] / 2)
            },

        }

        self.button_structure = {
            "B_Close": {
                "position": (WINDOW_SIZE[0] / 2 + 750, WINDOW_SIZE[1] / 2 + -400)
            },

            "B_NumDown": {
                "position": (WINDOW_SIZE[0] / 2 + 700, WINDOW_SIZE[1] / 2 + 10)
            },

            "B_NumUp": {
                "position": (WINDOW_SIZE[0] / 2 + 700, WINDOW_SIZE[1] / 2 - 10)
            },

            "B_Purchase": {
                "position": (WINDOW_SIZE[0] / 2 + 600, WINDOW_SIZE[1] / 2 + 200)
            },
        }

        self.text_structure = {
            "price": {
                "font": "OTF_Medium.otf",
                "font-size": 20,
                "text": "1개당 가격:    0원",
                "position": (WINDOW_SIZE[0] / 2 + 480, WINDOW_SIZE[1] / 2 -50),
                "color": (0, 0, 0)
            },

            "select_count_text": {
                "font": "OTF_Medium.otf",
                "font-size": 20,
                "text": "선택 수량:",
                "position": (WINDOW_SIZE[0] / 2 + 480, WINDOW_SIZE[1] / 2 - 10),
                "color": (0, 0, 0)
            },

            "select_count": {
                "font": "OTF_Bold.otf",
                "font-size": 30,
                "text": "1",
                "position": (WINDOW_SIZE[0] / 2 + 635, WINDOW_SIZE[1] / 2 - 15),
                "color": (255, 255, 255)
            },

            "total_price": {
                "font": "OTF_Medium.otf",
                "font-size": 20,
                "text": "최종 가격:    0원",
                "position": (WINDOW_SIZE[0] / 2 + 480, WINDOW_SIZE[1] / 2 + 30),
                "color": (0, 0, 0)
            },
        }

        shop_scroll = Scroll((1000, 700), direction="v")
        shop_scroll.rect.center = (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2)

        self.scroll_structure = {
            "shop_scroll": shop_scroll
        }

        self.load_guis()

    def update_select(self, selected_machine, select_count):
        if select_count != self.select_count:
            self.select_count = select_count
            for text in self.texts:
                if text.name == "total_price":
                    text.text = f"최종 가격:    {(shop_items[self.selected_machine] if self.selected_machine != None else 0) * self.select_count}원"
                elif text.name == "select_count":
                    text.text = str(self.select_count)
        if selected_machine != None:
            
            if selected_machine != self.selected_machine:
                if self.selected_machine != None:
                    for frame in self.frames:
                        if frame.name == self.selected_machine + "_Select":
                            self.frames.remove(frame)
                            break
                self.selected_machine = selected_machine
                new_selected_machine_frame = Frame(Texture.from_surface(self.app[1], shop_select_images[selected_machine]))
                new_selected_machine_frame.name = selected_machine + "_Select"
                new_selected_machine_frame.rect.center = self.selected_machine_position
                self.frames.append(new_selected_machine_frame)

                for text in self.texts:
                    if text.name == "price":
                        text.text = f"1개당 가격:    {shop_items[self.selected_machine]}원"
                    elif text.name == "select_count":
                        text.text = str(self.select_count)
                    elif text.name == "total_price":
                        text.text = f"최종 가격:    {shop_items[self.selected_machine] * self.select_count}원"

        if selected_machine == None:
            if self.selected_machine != None:
                for frame in self.frames:
                    if frame.name == self.selected_machine + "_Select":
                        self.frames.remove(frame)
                        break
                
                self.selected_machine = None
                self.select_count = select_count
                for text in self.texts:
                    if text.name == "price":
                        text.text = f"1개당 가격:    0원"
                    elif text.name == "select_count":
                        text.text = str(self.select_count)
                    elif text.name == "total_price":
                        text.text = f"최종 가격:    0원"