import pygame
from settings import *
from objects import Conveyer

class Edit:
    def __init__(self, conveyer: Conveyer) -> None:
        self.display_surf = pygame.display.get_surface()
        self.conveyer = conveyer

    def run(self, floor_objects, offset):

        for floor in floor_objects:
            if floor.real_rect.collidepoint(pygame.mouse.get_pos()):
                self.conveyer.rect.topleft = floor.real_rect.topleft

        self.display_surf.blit(self.conveyer.image, self.conveyer.rect)