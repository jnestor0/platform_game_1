import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_projectile_callback):
        super().__init__()
        self.create_projectile = create_projectile_callback
        self.facing_dir = 1
        self.ready_to_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 300
        
        self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_timer = 0.0
        
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
            
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            
        if keys[pygame.K_f] and self.can_fire and self.ready_to_shoot:
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
        self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        
        if p_type == 'size':
            self.is_big = True
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.Surface(PLAYER_POWERUP_SIZE, pygame.SRCALPHA)
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
                self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
                self.rect = self.image.get_rect(bottomleft=(left, bottom))

    def recharge(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready_to_shoot = True

    def animate(self):
        self.image.fill((0, 0, 0, 0)) # clear frame
        
        if self.direction.x != 0 and self.on_ground:
            self.animation_timer += 0.2
        elif not self.on_ground:
            self.animation_timer = math.pi / 4
        else:
            self.animation_timer = 0
            
        swing = math.sin(self.animation_timer) * 30 
        
        size = PLAYER_POWERUP_SIZE if self.is_big else PLAYER_SIZE
        center_x = size[0] // 2
        
        head_pos = (center_x, 10 if not self.is_big else 15)
        pelvis_pos = (center_x, 25 if not self.is_big else 40)
        shoulder_pos = (center_x, 15 if not self.is_big else 22)
        
        color = PLAYER_COLOR
        
        pygame.draw.circle(self.image, color, head_pos, 8 if not self.is_big else 12)
        pygame.draw.line(self.image, color, head_pos, pelvis_pos, 4)
        
        leg_length = 15 if not self.is_big else 20
        ll_x = pelvis_pos[0] + math.sin(math.radians(swing)) * leg_length
        ll_y = pelvis_pos[1] + math.cos(math.radians(swing)) * leg_length
        pygame.draw.line(self.image, color, pelvis_pos, (ll_x, ll_y), 4)
        
        rl_x = pelvis_pos[0] + math.sin(math.radians(-swing)) * leg_length
        rl_y = pelvis_pos[1] + math.cos(math.radians(-swing)) * leg_length
        pygame.draw.line(self.image, color, pelvis_pos, (rl_x, rl_y), 4)
        
        arm_length = 12 if not self.is_big else 18
        la_x = shoulder_pos[0] + math.sin(math.radians(-swing)) * arm_length
        la_y = shoulder_pos[1] + math.cos(math.radians(-swing)) * arm_length
        pygame.draw.line(self.image, color, shoulder_pos, (la_x, la_y), 3)
        
        ra_x = shoulder_pos[0] + math.sin(math.radians(swing)) * arm_length
        ra_y = shoulder_pos[1] + math.cos(math.radians(swing)) * arm_length
        pygame.draw.line(self.image, color, shoulder_pos, (ra_x, ra_y), 3)

    def update(self):
        self.get_input()
        self.recharge()
        self.update_powerups()
        self.animate()
