import pygame
from settings import *
from objects import Conveyer

direction_list = {
    "R": "B",
    "B": "L",
    "L": "T",
    "T": "R",
    "RT": "BR",
    "BR": "LB",
    "LB": "TL",
    "TL": "RT",
    "RB": "BL",
    "BL": "LT",
    "LT": "TR",
    "TR": "RB"
    
}

class Edit:
    def __init__(self, conveyer: Conveyer) -> None:
        self.display_surf = pygame.display.get_surface()
        self.conveyer = conveyer
        
        self.r_pressed = False
        

    def run(self, floor_objects, offset):
        self.conveyer.image.set_alpha(100)
        self.conveyer.rect.topleft = offset
        for floor in floor_objects:
            if floor.real_rect.collidepoint(pygame.mouse.get_pos()):
                self.conveyer.rect.topleft = floor.real_rect.topleft
                self.conveyer.position = floor.position

        keyboard = pygame.key.get_pressed()

        if keyboard[pygame.K_r] and not self.r_pressed:
            self.r_pressed = True
            self.conveyer.image = pygame.transform.rotate(self.conveyer.image, -90)
            self.conveyer.direction = direction_list[self.conveyer.direction]
            print(self.conveyer.direction)
        elif not keyboard[pygame.K_r]:
            self.r_pressed = False

        self.display_surf.blit(self.conveyer.image, self.conveyer.rect)