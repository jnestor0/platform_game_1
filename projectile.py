import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill(PROJECTILE_COLOR)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.direction = direction  # 1 for right, -1 for left
        
    def update(self):
        self.rect.x += self.speed * self.direction
        # Destroy if it goes completely off screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
