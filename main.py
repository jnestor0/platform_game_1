import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Power-Up Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level(self.screen)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        pass
        
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.level.run()
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
