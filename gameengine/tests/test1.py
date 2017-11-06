import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager

pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), 0, 32)

class Carre(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(50, 50)

        self.addComponent(CustomDraw)
        self.addComponent(Input)
        self.addScript(self)

    def onDraw(self):
        surface = pygame.Surface((50, 50))
        surface.fill((255, 255, 0))
        return surface

    def onMouseDrag(self, pos, rel, buttons):
        self.transform.position += rel

class Scene1(Scene):
    def onLoad(self):
        Carre()

SceneManager().loadScene(Scene1)


while True:
    World.update()
    World.draw()
    clock.tick(60)
