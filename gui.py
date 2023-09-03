import pygame
from settings import *

class GUI(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface) -> None:
        super().__init__()
        self.image = surf
        self.name = ""
        self.rect = surf.get_bounding_rect()
        

class Frame(GUI):
    def __init__(self, surf) -> None:
        super().__init__(surf)

class Button(GUI):
    def __init__(self, surf) -> None:
        super().__init__(surf)

class Text():
    def __init__(self, font, font_size, text, position) -> None:
        self.font_size = font_size
        self.text = text
        self.position = position

        self.font = pygame.font.Font(f"./font/{font}", font_size)
    
    def render(self):
        return self.font.render(self.text, True, (0, 0, 0))