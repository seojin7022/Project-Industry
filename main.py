import os, ctypes, json

with open(f"./requirements.txt", 'r') as requirements:
    for requirement in requirements.readlines():
       os.system(f"pip install {requirement}")

import init, cv2
import pygame, sys
from pygame._sdl2 import *
from settings import *
from level import Level
from lobby import Lobby

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

class Game: #게임 클래스
    def __init__(self) -> None:
        pygame.init()
        self.window = Window("나만의 공장", WINDOW_SIZE)
        self.window.maximize()
        
        self.renderer = Renderer(self.window)
        
        surf = pygame.Surface(WINDOW_SIZE)
        surf.fill((255,255,255))
        self.background = Texture.from_surface(self.renderer, surf)

        
        
        self.lobby = Lobby([self.window, self.renderer])
        self.level = Level([self.window, self.renderer, init.data, init.isFirstStarter])

        self.clock = pygame.time.Clock()

    def play_intro(self):
        video = cv2.VideoCapture("./img/LoadingScreen.mp4")
        ret, frame = video.read()
        while ret:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.renderer.clear()

            if ret:
                image = pygame.image.frombytes(frame.tobytes(), (1920, 1080), "RGB")
                self.renderer.blit(Texture.from_surface(self.renderer, image), pygame.Rect(0, 0, 1920 / self.renderer.scale[0], 1080 / self.renderer.scale[1]))
            ret, frame = video.read()

            self.renderer.present()
            self.clock.tick(FPS)
        
        return ret
    
    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.renderer.clear()
            self.renderer.blit(self.background, pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
            out = self.lobby.run()

            if out:
                return
            
            self.renderer.present()
            self.clock.tick(FPS)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("./data/player-data.txt", 'w') as PlayerData:
                        PlayerData.write(json.dumps(init.data))
                    pygame.quit()
                    sys.exit()

            
            self.renderer.clear()
            self.renderer.blit(self.background, pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
            self.level.run()
            
            self.renderer.present()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.play_intro()
    game.main()
    game.run()
