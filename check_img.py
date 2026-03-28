import pygame
import sys

pygame.init()

p = r"C:\Users\jnest\.gemini\antigravity\brain\a5ca52f3-1f57-4659-8658-31c2cc7dba40\plumber_sprite_1774669742984.png"
d = r"C:\Users\jnest\.gemini\antigravity\brain\a5ca52f3-1f57-4659-8658-31c2cc7dba40\dragon_enemy_1774669282623.png"

for name, path in [("Plumber", p), ("Dragon", d)]:
    i = pygame.image.load(path)
    print(name, "top left:", i.get_at((0,0)))
    print(name, "samples:", [tuple(i.get_at((x,0))) for x in range(0, 50, 10)])
