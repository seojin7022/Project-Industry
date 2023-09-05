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
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        
        
        

        self.level = Level()

        self.clock = pygame.time.Clock()
        
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            # self.renderer.clear()
            self.level.run()
            pygame.display.update()
            # self.renderer.present()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
