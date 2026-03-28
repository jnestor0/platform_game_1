import pygame
from settings import PLATFORM_COLOR, LEVEL_WIDTH, HEIGHT, WIDTH, TEXT_COLOR
from player import Player
from enemy import Enemy
from powerups import PowerUp, Coin
from projectile import Projectile

LEVEL_MAPS = {
    1: {
        "platforms": [
            (0, 560, 800, 40),
            (950, 560, 600, 40),
            (1700, 560, 1300, 40),
            (400, 460, 150, 20),
            (650, 360, 150, 20),
            (1100, 400, 200, 20),
            (1450, 300, 150, 20),
            (1850, 430, 150, 20),
            (2100, 330, 150, 20),
        ],
        "enemies": [(450, 420, 50), (1200, 360, 80), (1900, 390, 50)],
        "powerups": [((700, 340), "fire"), ((1500, 280), "speed")],
        "coins": [
            (410, 430),
            (440, 430),
            (470, 430),
            (680, 330),
            (710, 330),
            (1150, 370),
            (1200, 370),
        ],
    },
    2: {
        "platforms": [
            (0, 560, 600, 40),
            (750, 560, 500, 40),
            (1400, 560, 800, 40),
            (2350, 560, 650, 40),
            (300, 450, 150, 20),
            (550, 350, 150, 20),
            (900, 250, 150, 20),
            (1500, 400, 200, 20),
            (1800, 280, 150, 20),
            (2100, 180, 150, 20),
        ],
        "enemies": [(350, 410, 50), (950, 210, 50), (1600, 360, 80), (2400, 520, 100)],
        "powerups": [((600, 330), "size"), ((1850, 260), "fire")],
        "coins": [
            (320, 420),
            (350, 420),
            (570, 320),
            (600, 320),
            (920, 220),
            (950, 220),
            (1550, 370),
        ],
    },
    3: {
        "platforms": [
            (0, 560, 500, 40),
            (650, 560, 400, 40),
            (1200, 560, 400, 40),
            (1750, 560, 1250, 40),
            (250, 440, 100, 20),
            (450, 320, 100, 20),
            (750, 220, 100, 20),
            (1050, 320, 100, 20),
            (1350, 420, 100, 20),
            (1600, 300, 100, 20),
            (1950, 200, 150, 20),
            (2250, 350, 150, 20),
        ],
        "enemies": [
            (250, 400, 20),
            (750, 180, 20),
            (1350, 380, 20),
            (2000, 160, 50),
            (2300, 310, 50),
        ],
        "powerups": [
            ((480, 300), "speed"),
            ((1630, 280), "size"),
            ((2030, 180), "fire"),
        ],
        "coins": [
            (260, 410),
            (460, 290),
            (760, 190),
            (1060, 290),
            (1360, 390),
            (1610, 270),
            (1970, 170),
        ],
    },
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
        self.camera_scroll = 0
        self.build_level()

    def build_level(self):
        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        # Create player
        player_sprite = Player((100, 300), self.create_projectile)
        self.player.add(player_sprite)

        level_data = LEVEL_MAPS[self.current_level]

        # Create platforms
        for p in level_data["platforms"]:
            self.platforms.add(Platform(*p))

        # Create enemies
        for e in level_data["enemies"]:
            self.enemies.add(Enemy((e[0], e[1]), e[2]))

        # Create powerups
        for p in level_data["powerups"]:
            self.powerups.add(PowerUp(p[0], p[1]))

        # Create coins
        for c in level_data.get("coins", []):
            self.coins.add(Coin(c))

    def create_projectile(self, pos, direction):
        projectile = Projectile(pos, direction)
        self.projectiles.add(projectile)

    def check_collisions(self):
        player = self.player.sprite

        # Coins
        collided_coins = pygame.sprite.spritecollide(player, self.coins, True)
        for coin in collided_coins:
            player.score += 1

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
        if player.rect.right >= LEVEL_WIDTH - 50:
            self.current_level += 1
            if self.current_level > len(LEVEL_MAPS):
                self.current_level = 1
            self.build_level()

        # Check deaths (falling off map)
        if player.rect.top > HEIGHT:
            player.rect.topleft = (100, 300)
            self.camera_scroll = 0

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
        self.coins.update()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.check_collisions()

        # update camera
        player_sprite = self.player.sprite
        self.camera_scroll = player_sprite.rect.centerx - WIDTH // 2
        if self.camera_scroll < 0:
            self.camera_scroll = 0
        elif self.camera_scroll > LEVEL_WIDTH - WIDTH:
            self.camera_scroll = LEVEL_WIDTH - WIDTH

        # draw level
        for group in [
            self.platforms,
            self.powerups,
            self.enemies,
            self.projectiles,
            self.coins,
        ]:
            for sprite in group.sprites():
                self.display_surface.blit(
                    sprite.image, (sprite.rect.x - self.camera_scroll, sprite.rect.y)
                )

        self.display_surface.blit(
            player_sprite.image,
            (player_sprite.rect.x - self.camera_scroll, player_sprite.rect.y),
        )

        # UI
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f"Level: {self.current_level}", True, TEXT_COLOR)
        self.display_surface.blit(level_text, (10, 10))

        score_text = font.render(f"Score: {player_sprite.score}", True, TEXT_COLOR)
        self.display_surface.blit(score_text, (10, 40))

        if player_sprite.is_big or player_sprite.is_fast or player_sprite.can_fire:
            time_left = max(
                0,
                (
                    player_sprite.powerup_duration
                    - (pygame.time.get_ticks() - player_sprite.powerup_start_time)
                )
                // 1000,
            )
            active_p = (
                "Size"
                if player_sprite.is_big
                else "Speed" if player_sprite.is_fast else "Fire"
            )
            p_text = font.render(
                f"Powerup: {active_p} ({time_left}s)", True, TEXT_COLOR
            )
            self.display_surface.blit(p_text, (10, 70))
