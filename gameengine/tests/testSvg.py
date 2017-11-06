import pygame

from gameengine.core.World import World
from gameengine.util.util import svgToSurface

pygame.init()
clock = pygame.time.Clock()
World.display = pygame.display.set_mode((800, 464), 0, 32)

svg = svgToSurface("../ui/res/checkbox-unchecked.svg", 100, 100)
png = pygame.image.load("../ui/res/checkbox-unchecked.png").convert_alpha()

newPng = pygame.transform.smoothscale(png, (200, 100))

svg = svgToSurface("../ui/res/slider-bg.svg", 100, 100)

while True:
    # World.update()
    # World.draw()
    World.display.fill((255, 255, 255))
    World.display.blit(svg, (0, 0))
    pygame.display.flip()

    clock.tick(60)