import os

with open(f"./requirements.txt", 'r') as requirements:
    for requirement in requirements.readlines():
       os.system(f"pip install {requirement}") 
import pygame, sys
from pygame._sdl2 import *
from settings import *
from level import Level

class Game: #게임 클래스
    def __init__(self) -> None:
        pygame.init()
        self.window = Window("Factory", WINDOW_SIZE, fullscreen_desktop=True)
        self.renderer = Renderer(self.window)
        
        

        self.level = Level([self.window, self.renderer])

        self.clock = pygame.time.Clock()
        
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.renderer.clear()
            self.level.run()
            
            self.renderer.present()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
