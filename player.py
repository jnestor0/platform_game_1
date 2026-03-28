import pygame
import math
import os
from settings import (
    PLAYER_POWERUP_SIZE,
    PLAYER_SIZE,
    PLAYER_SPEED,
    GRAVITY,
    PLAYER_JUMP_SPEED,
    TERMINAL_VELOCITY,
    PLAYER_SPEED_BOOST,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_projectile_callback):
        super().__init__()
        self.create_projectile = create_projectile_callback
        self.facing_dir = 1
        self.ready_to_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 300

        image_path = r"C:\Users\jnest\.gemini\antigravity\brain\a5ca52f3-1f57-4659-8658-31c2cc7dba40\plumber_sprite_clean_1774670309850.png"
        self.base_image = None
        self.base_image_big = None
        if os.path.exists(image_path):
            temp_image = pygame.image.load(image_path).convert_alpha()
            temp_image = pygame.transform.scale(temp_image, PLAYER_POWERUP_SIZE)
            bg_color = temp_image.get_at((0, 0))
            w, h = PLAYER_POWERUP_SIZE
            magic_pink = (255, 0, 255)
            for x in range(w):
                for y in range(h):
                    c = temp_image.get_at((x, y))
                    # Erase background color matching top-left, AND any light grey/white checkerboard noises
                    is_bg = (
                        abs(c.r - bg_color.r) < 50
                        and abs(c.g - bg_color.g) < 50
                        and abs(c.b - bg_color.b) < 50
                    )
                    is_checkerboard = (
                        c.r > 170
                        and c.g > 170
                        and c.b > 170
                        and abs(c.r - c.g) < 30
                        and abs(c.r - c.b) < 30
                    )
                    if is_bg or is_checkerboard:
                        temp_image.set_at((x, y), magic_pink)

            temp_image.set_colorkey(magic_pink)
            self.base_image_big = temp_image
            self.base_image = pygame.transform.scale(temp_image, PLAYER_SIZE)
            self.base_image.set_colorkey(magic_pink)
            self.image = self.base_image.copy()
        else:
            self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)

        self.rect = self.image.get_rect(topleft=pos)
        self.animation_timer = 0.0
        self.score = 0

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
            spawn_pos = (
                self.rect.midright if self.facing_dir == 1 else self.rect.midleft
            )
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

        if p_type == "size":
            self.is_big = True
            bottom = self.rect.bottom
            left = self.rect.left
            if self.base_image_big:
                self.image = self.base_image_big.copy()
            elif self.base_image:
                self.image = pygame.transform.scale(
                    self.base_image, PLAYER_POWERUP_SIZE
                )
            else:
                self.image = pygame.Surface(PLAYER_POWERUP_SIZE, pygame.SRCALPHA)
            self.rect = self.image.get_rect(bottomleft=(left, bottom))
        else:
            self.image = (
                self.base_image.copy()
                if self.base_image
                else pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
            )

        if p_type == "speed":
            self.is_fast = True
            self.speed = PLAYER_SPEED_BOOST
        elif p_type == "fire":
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
                self.image = (
                    self.base_image.copy()
                    if self.base_image
                    else pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
                )
                self.rect = self.image.get_rect(bottomleft=(left, bottom))

    def recharge(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready_to_shoot = True

    def animate(self):
        if not self.base_image:
            return

        size = PLAYER_POWERUP_SIZE if self.is_big else PLAYER_SIZE
        current_base = (
            self.base_image_big
            if self.is_big and getattr(self, "base_image_big", None)
            else self.base_image
        )

        # Flip image based on facing
        if self.facing_dir == -1:
            flipped = pygame.transform.flip(current_base, True, False)
        else:
            flipped = current_base

        # Bobbing
        if self.direction.x != 0 and self.on_ground:
            self.animation_timer += 0.5
            bob = abs(math.sin(self.animation_timer)) * 4
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.blit(flipped, (0, -bob))
        else:
            self.animation_timer = 0
            self.image = flipped

    def update(self):
        self.get_input()
        self.recharge()
        self.update_powerups()
        self.animate()
