import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_projectile_callback):
        super().__init__()
        self.create_projectile = create_projectile_callback
        self.facing_dir = 1
        self.ready_to_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 300
        
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
        
        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        
        # Player status
        self.on_ground = False
        
        # Powerup states
        self.powerup_timer = 0
        self.is_big = False
        self.is_fast = False
        self.can_fire = False
        self.powerup_duration = 5000  # 5 seconds
        self.powerup_start_time = 0
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_dir = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_dir = -1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
            
        if keys[pygame.K_SPACE] and self.can_fire and self.ready_to_shoot:
            spawn_pos = self.rect.midright if self.facing_dir == 1 else self.rect.midleft
            self.create_projectile(spawn_pos, self.facing_dir)
            self.ready_to_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        if self.direction.y > TERMINAL_VELOCITY:
            self.direction.y = TERMINAL_VELOCITY
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
        
    def activate_powerup(self, p_type):
        self.powerup_start_time = pygame.time.get_ticks()
        self.is_big = False
        self.is_fast = False
        self.can_fire = False
        
        self.speed = PLAYER_SPEED  # reset
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOR)
        
        if p_type == 'size':
            self.is_big = True
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.Surface(PLAYER_POWERUP_SIZE)
            self.image.fill(PLAYER_COLOR)
            self.rect = self.image.get_rect(bottomleft=(left, bottom))
        elif p_type == 'speed':
            self.is_fast = True
            self.speed = PLAYER_SPEED_BOOST
        elif p_type == 'fire':
            self.can_fire = True
            
    def update_powerups(self):
        if self.is_big or self.is_fast or self.can_fire:
            current_time = pygame.time.get_ticks()
            if current_time - self.powerup_start_time >= self.powerup_duration:
                # Revert
                self.is_big = False
                self.is_fast = False
                self.can_fire = False
                self.speed = PLAYER_SPEED
                
                bottom = self.rect.bottom
                left = self.rect.left
                self.image = pygame.Surface(PLAYER_SIZE)
                self.image.fill(PLAYER_COLOR)
                self.rect = self.image.get_rect(bottomleft=(left, bottom))

    def recharge(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready_to_shoot = True

    def update(self):
        self.get_input()
        self.recharge()
        self.update_powerups()
