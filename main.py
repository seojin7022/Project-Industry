import pygame, sys
from settings import *

class Game: #게임 클래스
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
