import pygame, math
from settings import *
from gamemath import *
class GUI(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, name="") -> None:
        super().__init__()
        self.image = surf
        self.name = name
        self.rect = surf.get_rect()
        

class Frame(GUI):
    def __init__(self, surf) -> None:
        super().__init__(surf)

class Button(GUI):
    def __init__(self, surf, hover_surf = None) -> None:
        super().__init__(surf)
        self.hover_image = hover_surf

    def hover(self):
        pass

class Text():
    def __init__(self, font, font_size, text, position) -> None:
        self.font_size = font_size
        self.text = text
        self.position = position

        self.font = pygame.font.Font(f"./font/{font}", font_size)
    
    def render(self):
        return self.font.render(self.text, True, (0, 0, 0))
    
class Scroll(GUI):
    def __init__(self, size, direction="h") -> None:
        super().__init__(pygame.Surface(size))
        self.children = []
        self.offset = [0, 1]
        self.direction = direction
        self.margin = (5, 5)
        self.prior_mouse_pos = pygame.mouse.get_pos()
    
    def add_children(self, child):
        self.children.append(child)
        child.rect.topleft = self.rect.topleft

    def drag(self, mouse):
        
        current_mouse_pos = pygame.mouse.get_pos()

        isGuiCollide = False

        if mouse[0]:
            if self.rect.collidepoint(current_mouse_pos):
                isGuiCollide = True
                if self.direction == "h":
                    

                    self.offset[0] += clamp(50, (current_mouse_pos[0] - self.prior_mouse_pos[0])) * 0.1

                    self.offset[0] = max(min(self.margin[0] * len(self.children), self.offset[0]), 0)

        if mouse[0] == 0:
            self.prior_mouse_pos = pygame.mouse.get_pos()
        
        return isGuiCollide

    def custom_draw(self):
        for child in self.children:
            child.rect.left = self.rect.left + self.offset[0] + 190 * (self.children.index(child))
            
            child.image.srcrect.width = (child.rect.right - self.rect.left) if child.rect.right > self.rect.left else 0