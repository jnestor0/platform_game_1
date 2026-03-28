import pygame
import os
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_distance=100):
        super().__init__()
        
        image_path = r"C:\Users\jnest\.gemini\antigravity\brain\a5ca52f3-1f57-4659-8658-31c2cc7dba40\dragon_enemy_1774669282623.png"
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + 40))
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill(ENEMY_COLOR)
            self.rect = self.image.get_rect(topleft=pos)
            
        self.original_image = self.image.copy()
        
        self.start_x = pos[0]
        self.patrol_distance = patrol_distance
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        
    def update(self):
        # Simple patrol logic
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.direction *= -1
            
        if self.direction == 1:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image
