import pygame
from settings import *
from player import Player
from enemy import Enemy
from powerups import PowerUp
from projectile import Projectile

LEVEL_MAPS = {
    1: {'platforms': [(0, 560, 800, 40), (300, 450, 200, 20), (500, 300, 200, 20)], 'enemies': [(400, 410, 100), (600, 260, 50)], 'powerups': [((200, 430), 'size'), ((350, 430), 'fire'), ((650, 280), 'speed')]},
    2: {'platforms': [(0, 560, 800, 40), (200, 450, 150, 20), (450, 350, 150, 20), (700, 250, 100, 20)], 'enemies': [(300, 410, 50), (600, 310, 100)], 'powerups': [((450, 330), 'fire')]},
    3: {'platforms': [(0, 560, 800, 40), (150, 480, 100, 20), (350, 380, 100, 20), (550, 280, 100, 20), (750, 180, 50, 20)], 'enemies': [(200, 440, 50), (450, 340, 50), (650, 240, 50)], 'powerups': [((350, 360), 'speed')]}
}

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.current_level = 1
        self.build_level()
        
    def build_level(self):
        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Create player
        player_sprite = Player((100, 300), self.create_projectile)
        self.player.add(player_sprite)
        
        level_data = LEVEL_MAPS[self.current_level]
        
        # Create platforms
        for p in level_data['platforms']:
            self.platforms.add(Platform(*p))
            
        # Create enemies
        for e in level_data['enemies']:
            self.enemies.add(Enemy((e[0], e[1]), e[2]))
            
        # Create powerups
        for p in level_data['powerups']:
            self.powerups.add(PowerUp(p[0], p[1]))

    def create_projectile(self, pos, direction):
        projectile = Projectile(pos, direction)
        self.projectiles.add(projectile)
        
    def check_collisions(self):
        player = self.player.sprite
        
        # Powerups
        collided_powerups = pygame.sprite.spritecollide(player, self.powerups, True)
        if collided_powerups:
            for p in collided_powerups:
                player.activate_powerup(p.p_type)
                
        # Enemies
        if pygame.sprite.spritecollide(player, self.enemies, False):
            # simple death mechanic, respawn
            player.rect.topleft = (100, 300)
            
        # Projectiles hitting enemies
        pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)
        
        # Level progression
        if player.rect.right >= WIDTH:
            self.current_level += 1
            if self.current_level > len(LEVEL_MAPS):
                self.current_level = 1
            self.build_level()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        player.on_ground = False
        for sprite in self.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        # update level
        self.player.update()
        self.enemies.update()
        self.powerups.update()
        self.projectiles.update()
        
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.check_collisions()
        
        # draw level
        self.platforms.draw(self.display_surface)
        self.powerups.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.projectiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        
        # UI
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f'Level: {self.current_level}', True, TEXT_COLOR)
        self.display_surface.blit(level_text, (10, 10))
        
        player_sprite = self.player.sprite
        if player_sprite.is_big or player_sprite.is_fast or player_sprite.can_fire:
            time_left = max(0, (player_sprite.powerup_duration - (pygame.time.get_ticks() - player_sprite.powerup_start_time)) // 1000)
            active_p = 'Size' if player_sprite.is_big else 'Speed' if player_sprite.is_fast else 'Fire'
            p_text = font.render(f'Powerup: {active_p} ({time_left}s)', True, TEXT_COLOR)
            self.display_surface.blit(p_text, (10, 40))
