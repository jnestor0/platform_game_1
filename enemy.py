import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_distance=100):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
        
        self.start_x = pos[0]
        self.patrol_distance = patrol_distance
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        
    def update(self):
        # Simple patrol logic
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.direction *= -1
