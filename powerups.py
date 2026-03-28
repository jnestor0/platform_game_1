import pygame
from settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, p_type):
        super().__init__()
        self.p_type = p_type  # 'size', 'speed', or 'fire'
        self.image = pygame.Surface((20, 20))
        
        if self.p_type == 'size':
            self.image.fill(POWERUP_SIZE_COLOR)
        elif self.p_type == 'speed':
            self.image.fill(POWERUP_SPEED_COLOR)
        elif self.p_type == 'fire':
            self.image.fill(POWERUP_FIRE_COLOR)
            
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self):
        # We could add an oscillating floating animation here later
        pass
