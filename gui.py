import pygame, os
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
    def __init__(self, app, font, font_size, text, position, color, name) -> None:
        self.font_size = font_size
        self.text: str = text
        self.position = position
        self.app = app
        self.color = color
        self.font = pygame.font.Font(f"./font/{font}", font_size)
        self.name = name

        self.text_format = {
            "%Price%": shop_items
        }

    def render(self):
        return self.font.render(str(self.text), True, self.color)
    
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
                    

                    self.offset[0] += clamp(50, (current_mouse_pos[0] - self.prior_mouse_pos[0])) * 0.8

                    self.offset[0] = max(min(0, self.offset[0]), -500)

                elif self.direction == "v":
                    self.offset[1] += clamp(50, (current_mouse_pos[1] - self.prior_mouse_pos[1])) * 0.8

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


class GUIFrame(pygame.sprite.Group):
    def __init__(self, app, name) -> None:
        super().__init__()
        self.name = name
        self.frames = []
        self.buttons = []
        self.texts = []
        self.scrolls = []

        self.app = app

        self.frame_structure = {}
        self.button_structure = {}
        self.text_structure: {str: {str: str, str: str, str: tuple, str: tuple, str: int}} = {}
        self.scroll_structure = {}

    def load_guis(self):

        
        
        for frame, v in self.frame_structure.items():
            if type(v) == list:
                for i in v:

                    newFrame = Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/frame/{frame}.png")))
                    newFrame.name = frame
                    newFrame.rect.center = i["position"]
                    self.frames.append(newFrame)
            else:
                newFrame = Frame(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/frame/{frame}.png")))
                newFrame.name = frame
                newFrame.rect.center = v["position"]
                self.frames.append(newFrame)

        for button, v in self.button_structure.items():
            if type(v) == list:
                for i in v:
                    hover_img = None
                            
                    if os.path.exists(f"./gui/{self.name}/button/{button}_Hover.png"):
                        
                        hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}_Hover.png")))
                        
                    newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}.png"))), hover_img)
                    newButton.name = button
                    newButton.rect.center = i["position"]
                    self.buttons.append(newButton)
            else:
                hover_img = None
                    
                if os.path.exists(f"./gui/{self.name}/button/{button}_Hover.png"):
                    
                    hover_img = Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}_Hover.png")))
                    
                newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/button/{button}.png"))), hover_img)
                newButton.name = button
                newButton.rect.center = v["position"]
                self.buttons.append(newButton)

        for text_name, value in self.text_structure.items():
            font = value["font"]
            text = value["text"]
            position = value["position"]
            color = value["color"]
            font_size = value["font-size"]
            self.texts.append(Text(self.app, font, int(font_size), text, position, color, text_name))

        for scroll, value in self.scroll_structure.items():
            for button in os.listdir(f"./gui/{self.name}/scroll/{scroll}"):
                newButton = Button(Image(Texture.from_surface(self.app[1], pygame.image.load(f"./gui/{self.name}/scroll/{scroll}/{button}"))), None)
                newButton.name = button.split(".")[0]
                self.buttons.append(newButton)
                value.add_children(newButton)
            self.scrolls.append(value)

    def custom_draw(self):
        
        for scroll in self.scrolls:
            scroll.custom_draw()

        for frame in self.frames:
            self.app[1].blit(frame.image, frame.rect)

        for button in self.buttons:
            self.app[1].blit(button.image, button.rect)

        for text in self.texts:
            newRect = text.render().get_rect()
            newRect.topleft = text.position
            self.app[1].blit(Texture.from_surface(self.app[1], text.render()), newRect)