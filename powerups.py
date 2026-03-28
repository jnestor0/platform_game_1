import pygame
from settings import POWERUP_SIZE_COLOR, POWERUP_SPEED_COLOR, POWERUP_FIRE_COLOR


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, p_type):
        super().__init__()
        self.p_type = p_type  # 'size', 'speed', or 'fire'
        self.image = pygame.Surface((20, 20))

        if self.p_type == "size":
            self.image.fill(POWERUP_SIZE_COLOR)
        elif self.p_type == "speed":
            self.image.fill(POWERUP_SPEED_COLOR)
        elif self.p_type == "fire":
            self.image.fill(POWERUP_FIRE_COLOR)

        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        # We could add an oscillating floating animation here later
        pass


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (7, 7), 7)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass
