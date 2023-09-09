import pygame
from pygame._sdl2 import *
from settings import *
from gamemath import *
from animation import *
class GUI(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, name="") -> None:
        super().__init__()
        self.image = surf
        self.name = name
        self.rect = surf.get_rect()
        self.origin_rect = self.rect.copy()
        

class Frame(GUI):
    def __init__(self, surf) -> None:
        super().__init__(surf)

class Button(GUI):
    def __init__(self, surf, hover_surf = None) -> None:
        super().__init__(surf)
        self.hover_image = hover_surf
        
        self.animation = Animation(self.hover_image)
        if type(self.hover_image) == Image:
            self.hover_image_rect = self.hover_image.get_rect()
            
            self.hover_image.alpha = 0
        self.hovering = False

    def hover(self, renderer, animation_sprites):
        
        if type(self.hover_image) == Image:
            if not self.animation.properties.get("Alpha") and not self.hovering:
                self.hovering = True
                self.animation.add_property("Alpha", 255, 150, self.hover_image.alpha)
                animation_sprites.add(self)
            self.hover_image_rect.topleft = self.rect.topleft
            renderer.blit(self.hover_image, self.hover_image_rect)

    def hover_out(self, renderer, animation_sprites):
        if type(self.hover_image) == Image:
            if not self.animation.properties.get("Alpha") and self.hovering:
                self.hovering = False
                self.animation.add_property("Alpha", 0, 150, self.hover_image.alpha)
                animation_sprites.add(self)
            self.hover_image_rect.topleft = self.rect.topleft
            renderer.blit(self.hover_image, self.hover_image_rect)
class Text():
    def __init__(self, app, font, font_size, text, position, color) -> None:
        self.font_size = font_size
        self.text: str = text
        self.position = position
        self.app = app
        self.color = color
        self.font = pygame.font.Font(f"./font/{font}", font_size)
        
    
    def render(self):
        text = self.text
        
        if "%Money%" in text:
            text = text.replace("%Money%", str(self.app[2]["Money"]))

        return self.font.render(text, True, self.color)
    
class Scroll(GUI):
    def __init__(self, size, direction="h", max_count = 1) -> None:
        super().__init__(pygame.Surface(size))
        self.children = []
        self.offset = [0, 0]
        self.direction = direction
        self.max_count = 4
        self.margin = (20, 20)
        self.prior_mouse_pos = pygame.mouse.get_pos()
    
    def add_children(self, child):
        self.children.append(child)
        child.rect.topleft = self.rect.topleft
        # if self.direction == "h":
        #     child.rect.centery = self.rect.centery
        

    def drag(self, mouse):
        
        current_mouse_pos = pygame.mouse.get_pos()

        isGuiCollide = False

        if mouse[0]:
            if self.rect.collidepoint(current_mouse_pos):
                isGuiCollide = True
                if self.direction == "h":
                    

                    self.offset[0] += clamp(50, (current_mouse_pos[0] - self.prior_mouse_pos[0])) * 0.2

                    self.offset[0] = max(min(0, self.offset[0]), -500)

                elif self.direction == "v":
                    self.offset[1] += clamp(50, (current_mouse_pos[1] - self.prior_mouse_pos[1])) * 0.2

                    self.offset[1] = max(min(0, self.offset[1]), -(int(len(self.children) / self.max_count)) * self.children[0].rect.height)

        if mouse[0] == 0:
            self.prior_mouse_pos = pygame.mouse.get_pos()
        
        return isGuiCollide

    def custom_draw(self):
        for child in self.children:
            child.rect.left = self.rect.left + self.offset[0] + (child.origin_rect.width + self.margin[0]) * (self.children.index(child))
            if self.direction == "v":
                child.rect.top = self.rect.top + self.offset[1] + (child.origin_rect.height + self.margin[1]) * int(self.children.index(child) / self.max_count)
            child.image.srcrect.width = child.origin_rect.width
            child.image.srcrect.height = child.origin_rect.height
            child.image.srcrect.left = 0
            child.image.srcrect.top = 0
            child.rect.width = child.image.srcrect.width
            child.rect.height = child.image.srcrect.height
            if child.rect.left < self.rect.left:
                child.image.srcrect.width = min(max((child.origin_rect.width - (self.rect.left - child.rect.left)), 0), child.origin_rect.width)
                child.rect.width = child.image.srcrect.width
                child.image.srcrect.left = (child.origin_rect.width - child.rect.width)
                child.rect.left = self.rect.left

            if child.rect.top < self.rect.top:
                child.image.srcrect.height = min(max((child.origin_rect.height - (self.rect.top - child.rect.top)), 0), child.origin_rect.height)
                child.rect.height = child.image.srcrect.height
                child.image.srcrect.top = (child.origin_rect.height - child.rect.height)
                child.rect.top = self.rect.top
                