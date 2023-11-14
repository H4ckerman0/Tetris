import pygame, sys
from debug import debug
from settings import *
from level import Level

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.music = pygame.mixer.Sound(game_path + r"\audio\Tetris.ogg")
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu() 
            #self.screen.fill("#012c79")
            self.level.run()
            self.clock.tick(60)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()