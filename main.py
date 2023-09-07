import os, ctypes

with open(f"./requirements.txt", 'r') as requirements:
    for requirement in requirements.readlines():
       os.system(f"pip install {requirement}") 
import pygame, sys
from pygame._sdl2 import *
from settings import *
from level import Level

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

class Game: #게임 클래스
    def __init__(self) -> None:
        pygame.init()
        self.window = Window("Factory", WINDOW_SIZE)
        self.window.maximize()
        
        self.renderer = Renderer(self.window)
        
        surf = pygame.Surface(WINDOW_SIZE)
        surf.fill((255,255,255))
        self.background = Texture.from_surface(self.renderer, surf)
        

        self.level = Level([self.window, self.renderer])

        self.clock = pygame.time.Clock()
        
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.renderer.clear()
            self.renderer.blit(self.background, pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
            self.level.run()
            
            self.renderer.present()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
